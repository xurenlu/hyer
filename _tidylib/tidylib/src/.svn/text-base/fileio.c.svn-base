/* fileio.c -- does standard I/O

  (c) 1998-2003 (W3C) MIT, ERCIM, Keio University
  See tidy.h for the copyright notice.

  CVS Info :

    $LastChangedBy$ 
    $LastChangedDate$ 
    $LastChangedRevision$ 

  Default implementations of Tidy input sources
  and output sinks based on standard C FILE*.

*/

#include <stdio.h>

#include "fileio.h"
#include "tidy.h"


typedef struct _fp_input_source
{
    FILE*        fp;
    TidyBuffer   unget;
} FileSource;

int filesrc_getByte( ulong sourceData )
{
  FileSource* fin = (FileSource*) sourceData;
  int bv;
  if ( fin->unget.size > 0 )
    bv = tidyBufPopByte( &fin->unget );
  else
    bv = fgetc( fin->fp );
  return bv;
}
Bool filesrc_eof( ulong sourceData )
{
  FileSource* fin = (FileSource*) sourceData;
  Bool isEOF = ( fin->unget.size == 0 );
  if ( isEOF )
    isEOF = feof( fin->fp );
  return isEOF;
}
void filesrc_ungetByte( ulong sourceData, byte bv )
{
  FileSource* fin = (FileSource*) sourceData;
  tidyBufPutByte( &fin->unget, bv );
}

void initFileSource( TidyInputSource* inp, FILE* fp )
{
  FileSource* fin = NULL;

  inp->getByte    = filesrc_getByte;
  inp->eof        = filesrc_eof;
  inp->ungetByte  = filesrc_ungetByte;

  fin = (FileSource*) MemAlloc( sizeof(FileSource) );
  ClearMemory( fin, sizeof(FileSource) );
  fin->fp = fp;
  inp->sourceData = (ulong) fin;
}

void freeFileSource( TidyInputSource* inp, Bool closeIt )
{
    FileSource* fin = (FileSource*) inp->sourceData;
    if ( closeIt && fin && fin->fp )
      fclose( fin->fp );
    tidyBufFree( &fin->unget );
    MemFree( fin );
}

void filesink_putByte( ulong sinkData, byte bv )
{
  FILE* fout = (FILE*) sinkData;
  fputc( bv, fout );
}

void  initFileSink( TidyOutputSink* outp, FILE* fp )
{
  outp->putByte  = filesink_putByte;
  outp->sinkData = (ulong) fp;
}

