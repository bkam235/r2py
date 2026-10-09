  //   // jan01.kind == cctz::time_zone::civil_lookup::UNIQUE
  //   // jan01.pre    is 2011/01/01 00:00:00 -0800
  //   // jan01.trans  is 2011/01/01 00:00:00 -0800
  //   // jan01.post   is 2011/01/01 00:00:00 -0800
  //
  //   // A Spring DST transition, when there is a gap in civil time.
  //   auto mar13 = lax.lookup(cctz::civil_second(2011, 3, 13, 2, 15, 0));
  //   // mar13.kind == cctz::time_zone::civil_lookup::SKIPPED
  //   // mar13.pre   is 2011/03/13 03:15:00 -0700
  //   // mar13.trans is 2011/03/13 03:00:00 -0700
  //   // mar13.post  is 2011/03/13 01:15:00 -0800
  //
  //   // A Fall DST transition, when civil times are repeated.
  //   auto nov06 = lax.lookup(cctz::civil_second(2011, 11, 6, 1, 15, 0));
  //   // nov06.kind == cctz::time_zone::civil_lookup::REPEATED
  //   // nov06.pre   is 2011/11/06 01:15:00 -0700
  //   // nov06.trans is 2011/11/06 01:00:00 -0800
  //   // nov06.post  is 2011/11/06 01:15:00 -0800
  struct civil_lookup {
    enum civil_kind {
      UNIQUE,    // the civil time was singular (pre == trans == post)
      SKIPPED,   // the civil time did not exist (pre >= trans > post)
      REPEATED,  // the civil time was ambiguous (pre < trans <= post)
    } kind;
    time_point<seconds> pre;    // uses the pre-transition offset
    time_point<seconds> trans;  // instant of civil-offset change
    time_point<seconds> post;   // uses the post-transition offset
  };
