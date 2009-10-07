#include <buffio.h>
#include <stdio.h>
#include <errno.h>
#include <string.h>
#include "tidy-int.h"
#include "parser.h"
#include "clean.h"
#include "config.h"
#include "message.h"
#include "pprint.h"
#include "entities.h"
#include "tmbstr.h"
#include "utf8.h"

#ifdef TIDY_WIN32_MLANG_SUPPORT
#include "win32tc.h"
#endif

#ifdef NEVER
TidyDocImpl* tidyDocToImpl( TidyDoc tdoc )
{
  return (TidyDocImpl*) tdoc;
}
TidyDoc      tidyImplToDoc( TidyDocImpl* impl )
{
  return (TidyDoc) impl;
}

Node*        tidyNodeToImpl( TidyNode tnod )
{
  return (Node*) tnod;
}
TidyNode     tidyImplToNode( Node* node )
{
  return (TidyNode) node;
}

AttVal*      tidyAttrToImpl( TidyAttr tattr )
{
  return (AttVal*) tattr;
}
TidyAttr     tidyImplToAttr( AttVal* attval )
{
  return (TidyAttr) attval;
}

const TidyOptionImpl* tidyOptionToImpl( TidyOption topt )
{
  return (const TidyOptionImpl*) topt;
}
TidyOption   tidyImplToOption( const TidyOptionImpl* option )
{
  return (TidyOption) option;
}
#endif

void tidyGetTextNodeText2(TidyDoc tdoc,TidyNode tnod){

    TidyBuffer buf;
    tidyBufInit(&buf);
    tidyNodeGetText(tdoc, tnod, &buf);
    printf("hahaha%s\n", buf.bp?(char *)buf.bp:"");
    //printf("%*.*s\n", indent, indent, buf.bp?(char *)buf.bp:"");
    tidyBufFree(&buf);
/**
    TidyDocImpl * tim;
    tim = tidyDocToImpl(tdoc); 
    int size=0;
    Node * node;
    node = tidyNodeToImpl(tnod);
    size=node->end-node->start;
    if(size>0){
        char * p1;
        p1=(char * ) malloc( sizeof(char) * (size+1) );
        strncat(p1,tim->lexer->lexbuf+node->start,size);
        return p1;
    }
    else{
        return NULL;
    }
*/
}
void tidyFreePtr2(void * p){
//#if(p!=NULL)
//        free(p);
}
void dumpNode( TidyDoc tdoc,TidyNode tnod, int indent )
{
  TidyDocImpl * tim;
  TidyNode child;
  tim = tidyDocToImpl(tdoc); 
  int i=0;
  int size=0;

    Node * node;
    node = tidyNodeToImpl(tnod);
    size=node->end-node->start;
    /**
    if(size>0){
        char * p1;
        p1=(char * ) malloc( sizeof(char) * (size+1) );
        strncat(p1,tim->lexer->lexbuf+node->start,size);
        printf("new string:%s\n",p1);
        free(p1);
    } */
    //for( i=node->start;i<node->end;i++) {
    //   printf("%c",tim->lexer->lexbuf[i]);
    //}

    printf("\n\n");
  for ( child = tidyGetChild(tnod); child; child = tidyGetNext(child) )
  {
    ctmbstr name;
    if (tidyNodeGetType(child)==TidyNode_Text){
          name = tidyNodeGetName( child );
          printf( "we got an text node:\%*.*sNode: \%s\\n\n\n", indent, indent, " ", name );
    tidyGetTextNodeText2(tdoc,child);
     //   printf("\n\t year:%s",text);
      //  tidyFreePtr2(text);

    }
    switch ( tidyNodeGetType(child) )
    {
    case TidyNode_Root:       name = "Root";                    break;
    case TidyNode_DocType:    name = "DOCTYPE";                 break;
    case TidyNode_Comment:    name = "Comment";                 break;
    case TidyNode_ProcIns:    name = "Processing Instruction";  break;
    case TidyNode_Text:       name = "Text";                    break;
    case TidyNode_CDATA:      name = "CDATA";                   break;
    case TidyNode_Section:    name = "XML Section";             break;
    case TidyNode_Asp:        name = "ASP";                     break;
    case TidyNode_Jste:       name = "JSTE";                    break;
    case TidyNode_Php:        name = "PHP";                     break;
    case TidyNode_XmlDecl:    name = "XML Declaration";         break;

    case TidyNode_Start:
    case TidyNode_End:
    case TidyNode_StartEnd:
    default:
      name = tidyNodeGetName( child );
      break;
    }
    assert( name != NULL );
    //printf( "\%*.*sNode: \%s\\n\n", indent, indent, " ", name )a
    dumpNode(tdoc, child, indent + 4 );
  }
}

void dumpDoc( TidyDoc tdoc )
{
  dumpNode(tdoc, tidyGetRoot(tdoc), 0 );
}

void dumpBody( TidyDoc tdoc )
{
  dumpNode(tdoc, tidyGetBody(tdoc), 0 );
}


int main(int argc, char **argv )
{
  const char* input = "<div> \
        <div class='good'>  \
            <ul> \
                <li> \
                <a href='page2/list'>dos2</a> \
                <A href='page1/list'>dos1</A> \
                </li> \
            </ul> \
        </div> \ 
        <h3>haah </h3> \
        </div>  ";
  TidyBuffer output;
  TidyBuffer errbuf;
  int rc = -1;
  Bool ok;

  TidyDoc tdoc = tidyCreate();                     // Initialize "document"
  tidyBufInit( &output );
  tidyBufInit( &errbuf );
    //printf( "Tidying:\t\%s\\n", input );

  ok = tidyOptSetBool( tdoc, TidyXhtmlOut, yes );  // Convert to XHTML
  if ( ok )
    rc = tidySetErrorBuffer( tdoc, &errbuf );      // Capture diagnostics
  if ( rc >= 0 )
    rc = tidyParseString( tdoc, input );           // Parse the input
  if ( rc >= 0 )
    rc = tidyCleanAndRepair( tdoc );               // Tidy it up!
  if ( rc >= 0 )
    rc = tidyRunDiagnostics( tdoc );               // Kvetch
  if ( rc > 1 )                                    // If error, force output.
    rc = ( tidyOptSetBool(tdoc, TidyForceOutput, yes) ? rc : -1 );
  if ( rc >= 0 )
    rc = tidySaveBuffer( tdoc, &output );          // Pretty Print

  if ( rc >= 0 )
  {
    if ( rc > 0 )
      printf( "\\nDiagnostics:\\n\\n\%s", errbuf.bp );
    printf( "\\nAnd here is the result:\\n\\n\%s", output.bp );
  }
  else
    printf( "A severe error (\%d) occurred.\\n", rc );
  dumpDoc(tdoc);
  tidyBufFree( &output );
  tidyBufFree( &errbuf );
  tidyRelease( tdoc );
  return rc;
}


