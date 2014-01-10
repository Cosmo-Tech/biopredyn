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
  
#include "BioPreDyn/Types/BioPreDynEngineType.h"

namespace BioPreDyn {
    
namespace Types
{
  XSD::TypeDefinitionFactoryTmpl<XmlElement<BioPreDynEngineType> > BioPreDynEngineType::s_typeRegistry("BioPreDynEngineType", "urn:BioPreDyn");

  

  //constructor
  
  BioPreDynEngineType::BioPreDynEngineType(AnyTypeCreateArgs args):
  XMLSchema::Types::anyType(AnyTypeCreateArgs(false, 
                                              args.ownerNode, 
                                              args.ownerElem, 
                                              args.ownerDoc, 
                                              args.childBuildsTree, 
                                              (args.createFromElementAttr? false : args.abstract),
                                              args.blockMask,
                                              args.finalMask,
                                              args.contentTypeVariety,
                                              args.anyTypeUseCase,
                                              args.suppressTypeAbstract
                                             )),
    
    _fsmElems(NULL),
    _fsmAttrs(NULL)
  
    , _sequence(new sequence(this) )
  
  {
    this->contentTypeVariety(CONTENT_TYPE_VARIETY_ELEMENT_ONLY);
    initFSM();
    if(args.ownerDoc && args.ownerDoc->buildTree() && !args.childBuildsTree)
    {
      if(args.ownerDoc->createSample()) {
        _fsm->fireSampleEvents();
      }
      else {
        _fsm->fireRequiredEvents();
      }
    }
  }
    
  void BioPreDynEngineType::initFSM()
  {
    XsdFsmBasePtr fsmsAttrs[] = {
  
      NULL
    };

    _fsm->replaceOrAppendUniqueAttributeFsms(fsmsAttrs);
  
    _fsm->replaceContentFsm(_sequence);
      
    _fsmAttrs = _fsm->attributeFsm();
    _fsmElems = _fsm->contentFsm();

  }

  /* element functions  */
  

  BioPreDynEngineType::tool_ptr BioPreDynEngineType::create_tool(FsmCbOptions& options)
  {
    static DOMStringPtr myName = new DOMString("tool");
    static DOMStringPtr myNsUri = NULL;
    
    XSD::StructCreateElementThroughFsm t( myName, myNsUri, NULL, this->ownerElement(), this->ownerDocument(), _fsm, options, false, false, false, "urn:BioPreDyn", "ToolType");
    BioPreDynEngineType::tool_p node = XSD::createElementTmpl<tool, BioPreDyn::Types::ToolType*>(t);
          
    if(options.isSampleCreate && (node->stringValue() == "") ) {
      node->stringValue(node->sampleValue());
    }
    
    _tool = node;
      
    return node;
  }

  
  BioPreDynEngineType::tool_p BioPreDynEngineType::element_tool()
  {
    FSM::warnNullNode(_tool, "tool", "{urn:BioPreDyn}tool", 1);
    return _tool;
  }
    
  void BioPreDynEngineType::set_tool(DOMString val)
  {
    get_sequence()->set_tool(val);
  }

  DOMString BioPreDynEngineType::get_tool_string()
  {
    return get_sequence()->get_tool_string();
  }

          

  BioPreDynEngineType::argument_ptr BioPreDynEngineType::create_argument(FsmCbOptions& options)
  {
    static DOMStringPtr myName = new DOMString("argument");
    static DOMStringPtr myNsUri = NULL;
    
    XSD::StructCreateElementThroughFsm t( myName, myNsUri, NULL, this->ownerElement(), this->ownerDocument(), _fsm, options, false, false, false, "http://www.w3.org/2001/XMLSchema", "anyType");
    BioPreDynEngineType::argument_p node = XSD::createElementTmpl<argument, XMLSchema::Types::anyType*>(t);
          
    if(options.isSampleCreate && (node->stringValue() == "") ) {
      node->stringValue(node->sampleValue());
    }
    
    _list_argument.push_back(node);
      
    return node;
  }

  
  BioPreDynEngineType::argument_p BioPreDynEngineType::element_argument_at(unsigned int idx)
  {
    if(idx > _list_argument.size()-1) {
      throw IndexOutOfBoundsException("IndexOutOfBoundsException");
    }

    return _list_argument.at(idx);
  }
    
  List<BioPreDynEngineType::argument_ptr> BioPreDynEngineType::elements_argument()
  {
    return _list_argument;
  }
    
  BioPreDynEngineType::argument_p BioPreDynEngineType::add_node_argument()
  {
    return get_sequence()->add_node_argument();
  }

  List<BioPreDynEngineType::argument_ptr> BioPreDynEngineType::set_count_argument(unsigned int size)
  {
    return get_sequence()->set_count_argument(size);
  }

          

  /* attribute  functions  */
  
  //constructor
  BioPreDynEngineType::sequence::sequence(BioPreDynEngineType* that):
    _that(that)
  {
    XsdFsmBasePtr fsmArray[] = {
    new XsdFSM<tool_ptr>( Particle(NULL, DOMString("tool"), 1, 1), XsdEvent::ELEMENT_START, new object_unary_mem_fun_t<tool_ptr, BioPreDynEngineType, FsmCbOptions>(_that, &BioPreDynEngineType::create_tool)),
      new XsdFSM<argument_ptr>( Particle(NULL, DOMString("argument"), 0, -1), XsdEvent::ELEMENT_START, new object_unary_mem_fun_t<argument_ptr, BioPreDynEngineType, FsmCbOptions>(_that, &BioPreDynEngineType::create_argument)),
             
      NULL 
    } ;
    
    XsdSequenceFsmOfFSMs::init(fsmArray);
  }

      

  BioPreDynEngineType::tool_p BioPreDynEngineType::sequence::element_tool()
  {
      BioPreDynEngineType::tool_p node_p = NULL;
    XsdFsmBase* fsm_p = this->allFSMs()[0].get();
    if(fsm_p) 
    {
      XsdFSM<tool_ptr> *unitFsm = dynamic_cast<XsdFSM<tool_ptr> *>(fsm_p);
      if(unitFsm && unitFsm->nodeList().size()>0) {
        assert(unitFsm->nodeList().size()==1);  
        node_p = unitFsm->nodeList().at(0); 
      }
    }
    
    FSM::warnNullNode(node_p, "tool", "{urn:BioPreDyn}tool", 1);
    return node_p;
        
  }
  
  
  void BioPreDynEngineType::sequence::set_tool(DOMString val)
  {
      
    element_tool()->stringValue(val);
  }

  DOMString BioPreDynEngineType::sequence::get_tool_string()
  {
    return element_tool()->stringValue();
  }

          

  List<BioPreDynEngineType::argument_ptr> BioPreDynEngineType::sequence::elements_argument()
  {
      
    List<argument_ptr> nodeList;
    XsdFsmBase* fsm_p = this->allFSMs()[1].get();
    if(fsm_p) 
    {
      XsdFSM<argument_ptr> *unitFsm = dynamic_cast<XsdFSM<argument_ptr> *>(fsm_p);
      if(unitFsm) {
        //nodeList = unitFsm->nodeList().stl_list(); 
        nodeList = unitFsm->nodeList(); 
      }
    }
    return nodeList;
        
  }
  
  
  BioPreDynEngineType::argument_p BioPreDynEngineType::sequence::element_argument_at(unsigned int idx)
  {
    return elements_argument().at(idx);
  }

    
  BioPreDynEngineType::argument_p BioPreDynEngineType::sequence::add_node_argument()
  {
    DOMStringPtr nsUriPtr = NULL;
    XsdEvent event(nsUriPtr, NULL, DOMString("argument"), XsdEvent::ELEMENT_START, false);
    this->processEventThrow(event); 
    return elements_argument().back();
  }

  List<BioPreDynEngineType::argument_ptr> BioPreDynEngineType::sequence::set_count_argument(unsigned int size)
  {
    if( (size > -1) || (size < 0)) {
      ostringstream oss;
      oss << "set_count_argument: size should be in range: [" << 0
        << "," << "unbounded" << "]";
      throw IndexOutOfBoundsException(oss.str());
    }

    unsigned int prevSize = elements_argument().size();
    if(size < prevSize) {
      //FIXME: allow later:
      throw XPlus::RuntimeException("resize lesser than current size not allowed");
    }

    for(unsigned int j=prevSize; j<size; j++) 
    {
      // pretend docBuilding to avoid computation of adding after first loop
      XsdEvent event(NULL, NULL, DOMString("argument"), XsdEvent::ELEMENT_START, false);
      this->processEventThrow(event); 
    }
    
    return elements_argument();
  }

        
} //  end namespace Types 


} // end namespace BioPreDyn
