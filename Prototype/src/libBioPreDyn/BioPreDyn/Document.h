
 //
 //  This file was automatically generated using XmlPlus xsd2cpp tool.
 //  Please do not edit.
 //
  
#ifndef  __BioPreDyn_DOCUMENT_H__
#define  __BioPreDyn_DOCUMENT_H__
        
#include "XSD/xsdUtils.h"
#include "XSD/TypeDefinitionFactory.h"

#include "BioPreDyn/biopredyn_engine.h"
    

using namespace XPlus;
using namespace FSM;


namespace BioPreDyn {
    

class Document : public XMLSchema::TDocument
{
  private:
  
  
  biopredyn_engine_ptr _biopredyn_engine;
    
  AutoPtr<XsdFSM<biopredyn_engine_ptr> > _fsm_biopredyn_engine;
    
  
  // attributes, elements
  
  biopredyn_engine_ptr create_biopredyn_engine(FsmCbOptions& options);
  
  
  void initFSM();

  public:

  Document(bool buildTree=true, bool createSample=false);
  virtual ~Document() {}
    
  
  biopredyn_engine_p element_biopredyn_engine();
    
    
};

} // end namespace BioPreDyn
#endif
  