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
  
#ifndef  __BioPreDyn_types_BioPreDynEngineType_H__
#define  __BioPreDyn_types_BioPreDynEngineType_H__
#include "XSD/xsdUtils.h"
#include "XSD/TypeDefinitionFactory.h"


#include "BioPreDyn/Types/ToolType.h"
      
using namespace XPlus; 



namespace BioPreDyn {
    
namespace Types 
{
  
/// The class for complexType BioPreDynEngineType
/// \n Refer to documentation on structures/methods inside ...
class BioPreDynEngineType : public XMLSchema::Types::anyType
{
  public:
  //constructor
  BioPreDynEngineType(AnyTypeCreateArgs args);

  

  /// typedef for the Shared pointer to the node
  typedef AutoPtr<XMLSchema::XmlElement<BioPreDyn::Types::ToolType> > tool_ptr;
  /// typedef for the Plain pointer to the node
  typedef XMLSchema::XmlElement<BioPreDyn::Types::ToolType>* tool_p;
  
  /// typedef for the node
  typedef XMLSchema::XmlElement<BioPreDyn::Types::ToolType> tool; 
  

  /// typedef for the Shared pointer to the node
  typedef AutoPtr<XMLSchema::XmlElement<XMLSchema::Types::anyType> > argument_ptr;
  /// typedef for the Plain pointer to the node
  typedef XMLSchema::XmlElement<XMLSchema::Types::anyType>* argument_p;
  
  /// typedef for the node
  typedef XMLSchema::XmlElement<XMLSchema::Types::anyType> argument; 
  
  /// The MG class inside a complexType
  /// \n Refer to documentation on structures/methods inside ...
  struct sequence : public XsdSequenceFsmOfFSMs 
  {
      

    /// constructor for the MG node
    sequence(BioPreDynEngineType* that);

    

    ///  For the scalar-element with QName "{urn:BioPreDyn}tool" :
    ///  \n Returns the scalar element node
    ///  @return the element node fetched
    tool_p element_tool();

        

    ///  For the scalar-element with QName "{urn:BioPreDyn}tool" :
    ///  \n Sets the value of the scalar element with the supplied value.
    ///  @param val the value(as DOMString) to set with 
    void set_tool(DOMString val);

    ///  For the scalar-element with QName "{urn:BioPreDyn}tool" :
    ///  \n Returns the value of the scalar element 
    ///  @return the value(as DOMString) of the element 
    DOMString get_tool_string();

          

    ///  For vector-element with QName "{http://www.w3.org/2001/XMLSchema}argument" :
    ///  \n Returns the list of the element nodes
    ///  @return the list of element nodes fetched
    List<argument_ptr> elements_argument();

    ///  For vector-element with QName "{http://www.w3.org/2001/XMLSchema}argument" :
    ///  \n Returns the element node at supplied index
    ///  @param idx index of the element to fetch 
    ///  @return the element node fetched
    argument_p element_argument_at(unsigned int idx);

        

    ///  For vector-element with QName "{http://www.w3.org/2001/XMLSchema}argument" :
    ///  \n Adds one element to the end of the "list of the element nodes"
    ///  @return the pointer to the added element
    argument_p add_node_argument();

    ///  For vector-element with QName "{http://www.w3.org/2001/XMLSchema}argument" :
    ///  \n Sizes-up the "list of the element nodes" with the supplied size
    ///  @param size the request size(unsigned int) of the list
    ///  @return the list of "pointer-to-element-node"
    List<argument_ptr> set_count_argument(unsigned int size);


      

    //  accessors for MGs/MGDs which are nested children of this MG/MGD
    

  private:  

    inline XsdFsmBase* clone() const {
      return new sequence(*this);
    }

    BioPreDynEngineType*      _that;
  }; // end sequence
  

  ///  For the scalar-element with QName "{urn:BioPreDyn}tool" :
  ///  \n Returns the scalar element node
  ///  @return the element node fetched
  tool_p element_tool();
      

  ///  For the scalar-element with QName "{urn:BioPreDyn}tool" :
  ///  \n Sets the value of the element with the supplied value.
  ///  @param val the value(as DOMString) to set with 
  void set_tool(DOMString val);
  
  ///  For the scalar-element with QName "{urn:BioPreDyn}tool" :
  ///  \n Returns the value(as DOMString) of the element
  DOMString get_tool_string();

        

  ///  For vector-element with QName "{http://www.w3.org/2001/XMLSchema}argument" :
  ///  \n Returns the list of the element nodes
  ///  @return the list of element nodes fetched
  List<argument_ptr> elements_argument();

  ///  For vector-element with QName "{http://www.w3.org/2001/XMLSchema}argument" :
  ///  \n Returns the element node at supplied index
  ///  @param idx index of the element to fetch 
  ///  @return the element node fetched
  argument_p element_argument_at(unsigned int idx);

  

  ///  For vector-element with QName "{http://www.w3.org/2001/XMLSchema}argument" :
  ///  \n Adds one element to the end of the "list of the element nodes"
  ///  @return the pointer to the added element
  argument_p add_node_argument();
  
  ///  For vector-element with QName "{http://www.w3.org/2001/XMLSchema}argument" :
  ///  \n Sizes-up the "list of the element nodes" with the supplied size
  ///  @param size the request size(unsigned int) of the list
  ///  @return the list of "pointer-to-element-node"
  List<argument_ptr> set_count_argument(unsigned int size);

      

  /// Returns the MG node(or node-list) inside  the complexType 
  sequence*  get_sequence() {
    return _sequence;
  }

    

  protected:
  
  XsdAllFsmOfFSMsPtr   _fsmAttrs;   
  XsdFsmBasePtr        _fsmElems;   
  
  
  AutoPtr<sequence> _sequence;
    
    
  tool_ptr _tool;
            
  List<argument_ptr> _list_argument;
              

  /// initialize the FSM
  void initFSM();

  
  tool_ptr create_tool(FsmCbOptions& options);

  argument_ptr create_argument(FsmCbOptions& options);
  

public:

  //types which this class needs, as INNER CLASSES
  
  //types which this class needs, as INNER CLASSES : END

  

  private:
  static XSD::TypeDefinitionFactoryTmpl<XmlElement<BioPreDynEngineType> >   s_typeRegistry;
}; //end class BioPreDynEngineType
} // end namespace Types


} // end namespace BioPreDyn
#endif
  
