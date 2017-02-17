#!/usr/bin/perl

if (@ARGV != 1) {
   print "Please supply the directory to check.\n";
   exit(0);
}

$basedir = $ARGV[0];

opendir(CAMDIR,$basedir) or die "Cannot open base directory $basedir\n";
@camdirs = readdir(CAMDIR);

foreach $camdir (@camdirs) {

   if ($camdir ne "." and $camdir ne "..") {

   # if it's a directory, look in it
   if ( opendir(PIXDIR,$basedir."/".$camdir)) {

      @pixdirs = readdir(PIXDIR);

      # go through these subdirectories and make sure they're named right
      foreach $pixdir (@pixdirs) {

         if ($pixdir ne "." and $pixdir ne "..") {

         if ( opendir(FILDIR,$basedir."/".$camdir."/".$pixdir)) {

            if ($pixdir !~ m/$camdir_R\d/) {
               print "Problem with $camdir, subdirectory $pixdir\n";
            }

            # also look for AVI files
            @pixfiles = readdir(FILDIR);

            foreach $pixfile (@pixfiles) {
               if ($pixfile =~ m/AVI$/i) {
                  print "AVI files in $camdir, subdirectory $pixdir\n";
               }
            }
         }
         }


      }
   }
   }
}

