
 //
 //  This file was automatically generated using XmlPlus xsd2cpp tool.
 //  Please do not edit.
 //
  
#ifndef  __BioPreDyn_biopredyn_engine_H__
#define  __BioPreDyn_biopredyn_engine_H__
#include "XSD/UrTypes.h"
#include "XSD/xsdUtils.h"
#include "XSD/TypeDefinitionFactory.h"


#include "BioPreDyn/Types/BioPreDynEngineType.h"
      

using namespace XPlus;

namespace BioPreDyn {
    
  typedef XMLSchema::XmlElement<BioPreDyn::Types::BioPreDynEngineType> biopredyn_engine;
    

  //
  // Following types(mostly typedefs) are the ones, based on above C++ class definition
  // for the top-level element {urn:BioPreDyn}biopredyn-engine
  //


  /// typedef for the Shared pointer to the node
  typedef AutoPtr<XMLSchema::XmlElement<BioPreDyn::Types::BioPreDynEngineType> > biopredyn_engine_ptr;
  /// typedef for the Plain pointer to the node
  typedef XMLSchema::XmlElement<BioPreDyn::Types::BioPreDynEngineType>* biopredyn_engine_p;
  
  /// typedef for the node
  typedef XMLSchema::XmlElement<BioPreDyn::Types::BioPreDynEngineType> biopredyn_engine; 
  
} // end namespace BioPreDyn
#endif
