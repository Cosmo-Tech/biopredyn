/*=========================================================================

  Program: BioPreDyn Library (BioPreDyn)
  Language: C++
  $Author$
  $Date$
  $Revision$
  $Copyright: [2013] BioPreDyn $

=========================================================================*/
 //
 //  This file was automatically generated using XmlPlus xsd2cpp tool.
 //  Please do not edit.
 //
  
#ifndef __BioPreDyn_ToolType_H__ 
#define __BioPreDyn_ToolType_H__ 

#include <string>
#include <list>

#include "DOM/DOMCommonInc.h"
#include "XSD/PrimitiveTypes.h"
#include "XSD/xsdUtils.h"
#include "XSD/PrimitiveTypes.h"


using namespace std;
using namespace XPlus;
using namespace DOM;
using namespace XMLSchema;


namespace BioPreDyn {
    

namespace Types 
{
    

  /// class for simpleType with restriction on base
  class ToolType : public XMLSchema::Types::bt_string
  {
  public:
    /// constructor  
    ToolType(AnyTypeCreateArgs args)
    
        : bt_string(args)
      
    {
    

      vector<DOMString> values;
    
      values.push_back("COPASI");
    
      values.push_back("cobra");
    
      values.push_back("cellnopt.wrapper");
    
      values.push_back("libSBMLSim");
    
      _enumerationCFacet.value(values);
      
      this->appliedCFacets( appliedCFacets() | CF_ENUMERATION| CF_ENUMERATION| CF_ENUMERATION| CF_ENUMERATION );
    }
    
  protected:
    
  };

} // end namespace Types

} // end namespace BioPreDyn

#endif
  
