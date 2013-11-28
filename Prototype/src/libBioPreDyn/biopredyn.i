%module libbiopredyn
%{
#include "BioPreDyn/all-include.h"
%}

%include "XPlus/AutoPtr.h"
%include "XPlus/XPlusObject.h"
%include "DOM/DOMCommonInc.h"
%include "XPlus/Namespaces.h"
%include "XSD/FSM.h"
%include "XSD/UrTypes.h"
%include "XSD/TypeDefinitionFactory.h"
%include "XSD/SimpleTypeListTmpl.h"
%include "XSD/PrimitiveTypes.h"

%include "BioPreDyn/all-include.h"
%include "BioPreDyn/biopredyn_engine.h"
%include "BioPreDyn/Document.h"
%include "BioPreDyn/Types/BioPreDynEngineType.h"
%include "BioPreDyn/Types/ToolType.h"
