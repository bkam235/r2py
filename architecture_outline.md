Let's do a complete rework of the project. 
For this we need to prepare an architecture.md that we then put into a new folder and build a clean project from scratch. 
Inspect all MD-files to get context for this. 
Analyze the project thoroughly.
We won't use everything from the existing project. Old stage numbers might not map directly to new stage numbers below.
The new architecture must be clear, modular and extensible.

# Architectural outline:

## Stage 0 
Stage 0 should contain infrastructure for running R and Python scripts in their respective sandboxes. 
The sandboxes need to be fully comprehensive, capturing all main effects and side-effects of a script 
(think sandboxes used to train reinforcement learning agents for video games).
It also needs to contain everything to make scripts executable, e.g. package compilation and installation.
Stage 0 should also contain the current infrastructure for harvesting code examples to train the translator.

## Stage 1 
Stage 1 should perform the analytical preparation for translation. 
Its aim is a full understanding of what each element of the R script does when executed.
To achieve this, stage 1 should walk the AST tree of the R script.
For each branch, it should compile a (typed) list of all entities 
(e.g., but not limited to, variables, constants, functions, function calls) and all side effects 
(e.g., but not limited to, file I/O, graphics output, environment changes, printing, warning/error).
Stage 1 should do this even for unevaluated branches, e.g. false if-blocks or empty function calls.
To achieve this, stage 1 needs to run the full R script and/or parts of it.
To run unevaluated branches, stage 1 needs to extract a part of the R script, edit and run it.
All of these runs need to be done in the Stage 0 sandbox.
Some of the source code for entities used in the R script can reside in other R scripts or packages.
Stage 1 should look these up and include them (or where to find them) in its result.

At the end, stage 1 should produce a complete map of the R script, all its entities, their effects and side-effects.
Stage 1 should compute its coverage of the R code along the AST tree and continue its analysis until it has covered the complete tree.
Stage 1 should provide this map in a structured format, maybe as annotations to the R script, so that the translator can optimally consume it.

## Stages 2-4
These stages should form a self-improvement cycle.
Their interaction is a policy gradient loop over a symbolic policy.
This is closer to discrete/structured action RL (like AlphaCode's MCTS or RLHF with edits) than classical gradient descent.

The reward signal is sparse and expensive.
The accept/revert criterion (keep the update only if new_score >= current_score) is greedy hill-climbing RL.
Updates accepted for script A are baked into the policy before script B runs. 
This is online learning — the policy improves across episodes rather than being frozen. 
It also introduces a risk: an update that was good for script A might hurt script B (catastrophic forgetting / distribution shift).

Stage 2 provides an initial translation.
Stage 4 has the role of a reward model, performing execution equivalence testing.
Based on the signal from stage 4, stage 3 then develops editing tasks for the translation.
After editing in stage 3, stage 4 scores the edited translation again.
The cycle repeats until an early-stopping score threshold is met.
The translations, their edits and reward signals are recorded as structured, self-generated experience in the verification wiki.
The verification wiki (possibly enriched by what is currently capture in error_patterns.jsonl) can act as an informal replay buffer.
Over time, the translator should be able to handle increasingly complex translation tasks increasingly well.

## Stage 2
Stage 2 should perform the actual translation from R to Python.
This is a step-wise process based on the output from stage 1.
The goal of the translation is to have a Python script that has the best possible execution equivalence.
Execution equivalence means that the R script and its Python equivalent have the same effects and side-effects.
E.g. they produce the same data, or the same predictions, or the same plot, or the same file etc.

Execution equivalence does *not* mean that every entity in R and Python must be identical.
For example, an R script might fit a statistical model to data and output predicitions.
The fitting methods of the R model might differ from those in Python, but both models might still make the same or 
sufficiently similar predictions. Then the scripts still have execution equivalence.
Therefore, it's acceptable for execution equivalence that the R script and its Python translation use different libraries/packages.

The translation needs to be provided for the complete R script.
If the R script uses entities like functions or datasets from a package, the translator needs to look up the source code
and translate this, too. In this regard, the translated Python script goes beyond the original R script.
This functionality is currently contained in the old stage 1 as the sub-translation step. 

The translator is a self-improving system that learns to past successful translations.
Its knowledge is stored in a wiki with verified entries.
For this, we should replace the separate pairs DB and wiki with a single pattern library where every entry contains both guidance and empirical evidence.

Structure of one entry:
Pattern: <short name>
Package: <e.g. shiny>
Confidence: confirmed | tentative | contradicted
Guidance: <1-3 sentences explaining the rule and why it matters>
Evidence pairs:
  - <script name> → score <X> (path: <embedding|stdout+gate2>, variable: <name>)
Contradictions:
  - <script name> → score <X> (<brief note on what went wrong>)

Key design principles:
- Pairs are evidence, not the corpus. The LLM is shown guidance + supporting examples together, not raw pairs to copy. This prevents learning surface form without rationale.
- Adding a pair requires naming a pattern. Automatic accumulation on score-above-threshold is what caused past contamination with stub-based examples. Every new pair must be attributed to a named pattern; adding it is a claim that the pair demonstrates that pattern correctly.
- Package-level retrieval, not source similarity. Past Token Jaccard on R source finds scripts that look similar, not scripts that share translation challenges. Retrieve by package first, then by pattern relevance.
- Contradictions are first-class. When a translation follows a pattern's guidance and still scores below target, that is a contradiction, not just a missed score. The contradiction counter gives a real falsification signal and should trigger pattern review rather than blind instruction-appending.
- Later stages may only append to the contradiction log, never rewrite guidance. Guidance updates require a confirmed pattern (score above target, correct verification path, attribution of the relevant variable).

## Stage 3
Stage 3 should perform targeted edits of existing translations to improve execution equivalence.
Based on a translation from stage 2 and its execution equivalence score from stage 4, stage 3 should develop typed edits 
or combinations of typed edits to the translation that improve its score.

To know what it should edit, stage 3 needs to receive feedback from the stage 4 verifier (described below).
The feedback needs to be granular, which entity of the translation contributed to the score in which way, so that
the stage 3 editor can identify necessary changes to the translation. It might be helpful to decompose the score, i.e.:
- Did the Python script execute without error?
- Did shared entities have the right types?
- Did the control flow/AST tree match?
- Did data output match?
- Did variable output match?
- Did functional/callable output match?
- Did side-effects match?
- Did the LLM judge pass?

It might be necessary to have several iterations of successive edits and verification.
Each edit should know of previous edits and their verification feedback.
Like in machine learning/reinforcement learning, edits that raise the score should be pursued and memorized for future translations,
edits that lower the score should be reversed and discouraged for the future (see stage 2 verified wiki).
The top-level API of the r2py package should expose the number of allowed edit-verification iterations.
Iterations should stop early when a threshold score is reached. This threshold score should also be exposed by the top-level API.

The iterative edits need to balance exploration vs. exploitation.
It might be necessary to re-use some or all of the old stage 4 agent's capabilities for targeted edits.
However, the old stage 4 agent used a lot of tokens to understand previous translations (always beginning from scratch without guidance).
It also sometimes produced destructive outcomes, as documented in failure.md.
Look up these errors of the past to avoid them and develop a more efficient and effective solution.

## Stage 4
Stage 4 performs execution equivalence testing (=verifier) and shares its results with other stages as needed.
The verifier should have a modular, extensible architecture to accommodate different ways of equivalence testing.

The sandboxes from stage 0 should capture all main effects and side effects (including stdout and stderr) from the scripts.
Each type of captured effect should be normalized to a format that enable embedding comparison.
Currently, this format is JSON for data including text, and image comparison for plots.
It should probably also include HTML and/or markdown for other effect types like dashboards.

If no equivalence testing is possible, the fallback mechanism is a LLM judge.
The LLM judge should follow the guidance of the verified wiki in its judgments.
In past versions, the LLM judge pushes the editor towards exact re-implementations of R packages, 
even when equivalent python packages are available. That was the wrong approach.
Ideally, we don't need the LLM judge at all, if the sandboxes are really complete and capture ALL effects.

The verifier must also perform equivalence testing for parts of the code that are unevaluated, e.g. false if-blocks or uncalled functions.
For this, the verifier should be able to run parts of scripts with the state of the sandbox up to that point in the AST tree.
For RNG variables and data not available in both languages, the verifier can use the capture/replay mode.

The verifier should return how score decomposition by script entity to the other stages to provide granular signal.
The verifier should have a module that updates the verified wiki according to the epistemology rules.
This module should not only append to the wiki, but also remove or alter entries.
The update module should analyse the wiki for conflicts and resolve them, based on the epistemology rules.

## Work folder
Keep the existing examples from the input folder for training the translator.
Keep a script like translate.py to work through the examples folder.
Keep learning curve and scoring table analysis.