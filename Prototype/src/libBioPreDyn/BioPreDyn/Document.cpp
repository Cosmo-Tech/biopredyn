/*=========================================================================

  Program: BioPreDyn Library (BioPreDyn)
  Language: C++
  $Author$
  $Date$
  $Revision$
  $Copyright: [2013-2014] BioPreDyn $

=========================================================================*/
 //
 //  This file was automatically generated using XmlPlus xsd2cpp tool.
 //  Please do not edit.
 //
  
#include "BioPreDyn/Document.h"


namespace BioPreDyn {
    

  ///constructor for the Document node
  Document::Document(bool buildTree_, bool createSample_):
    XMLSchema::TDocument(buildTree_, createSample_)
  {
    initFSM();
    DOM::Document::attributeDefaultQualified(false);
    DOM::Document::elementDefaultQualified(false);
    
    if(buildTree()) 
    {
      
      DOMStringPtr nsUriPtr = new DOMString("urn:BioPreDyn");   
      XsdEvent event(nsUriPtr, NULL, DOMString("biopredyn-engine"), XsdEvent::ELEMENT_START);
      if(this->createSample()) {
        event.cbOptions.isSampleCreate = true;
      }
      _fsm->processEventThrow(event); 
      
    }
    
  }

  void Document::initFSM()
  {
  
    _fsm_biopredyn_engine = new XsdFSM<biopredyn_engine_ptr>( Particle(new DOMString("urn:BioPreDyn"),  DOMString("biopredyn-engine"), 1, 1),  XsdEvent::ELEMENT_START, new object_unary_mem_fun_t<biopredyn_engine_ptr, Document, FsmCbOptions>(this, &Document::create_biopredyn_engine));
  
    XsdFsmBasePtr elemFsms[] = {
    _fsm_biopredyn_engine,
      
      NULL
    };
    XsdFsmBasePtr fofElem = new XsdFsmOfFSMs(elemFsms, XsdFsmOfFSMs::CHOICE);
    
    XsdFsmBasePtr docEndFsm = new XsdFSM<void *>(Particle(NULL, "", 1, 1), XsdEvent::DOCUMENT_END);
    XsdFsmBasePtr ptrFsms[] = { fofElem,  docEndFsm, NULL };
    _fsm = new XsdFsmOfFSMs(ptrFsms, XsdFsmOfFSMs::SEQUENCE);
  }

  


  /* element functions  */
  

  biopredyn_engine_ptr Document::create_biopredyn_engine(FsmCbOptions& options)
  {
    static DOMStringPtr myName = new DOMString("biopredyn-engine");
    static DOMStringPtr myNsUri = new DOMString("urn:BioPreDyn");
    
    XSD::StructCreateElementThroughFsm t( myName, myNsUri, NULL, this, this, _fsm, options, false, false, false, "urn:BioPreDyn", "BioPreDynEngineType");
    biopredyn_engine_p node = XSD::createElementTmpl<biopredyn_engine, BioPreDyn::Types::BioPreDynEngineType*>(t);
          
    _biopredyn_engine = node;
      
    return node;
  }

  
  biopredyn_engine_p Document::element_biopredyn_engine()
  {
    FSM::warnNullNode(_biopredyn_engine, "biopredyn_engine", "{urn:BioPreDyn}biopredyn-engine", 1);
    return _biopredyn_engine;
  }
    
} // end namespace BioPreDyn
