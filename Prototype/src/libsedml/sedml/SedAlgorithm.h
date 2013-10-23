/**
 * @file:   SedAlgorithm.h
 * @brief:  Implementation of the SedAlgorithm class
 * @author: Frank T. Bergmann
 *
 * <!--------------------------------------------------------------------------
 * This file is part of libSEDML.  Please visit http://sed-ml.org for more
 * information about SEDML, and the latest version of libSEDML.
 *
 * Copyright (c) 2013, Frank T. Bergmann  
 * All rights reserved.
 * 
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met: 
 * 
 * 1. Redistributions of source code must retain the above copyright notice, this
 *    list of conditions and the following disclaimer. 
 * 2. Redistributions in binary form must reproduce the above copyright notice,
 *    this list of conditions and the following disclaimer in the documentation
 *    and/or other materials provided with the distribution. 
 * 
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
 * ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
 * ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 * ------------------------------------------------------------------------ -->
 */


#ifndef SedAlgorithm_H__
#define SedAlgorithm_H__


#include <sedml/common/extern.h>
#include <sedml/common/sedmlfwd.h>


#ifdef __cplusplus


#include <string>


#include <sedml/SedBase.h>
#include <sedml/SedListOf.h>
#include <sedml/SedNamespaces.h>


LIBSEDML_CPP_NAMESPACE_BEGIN




class LIBSEDML_EXTERN SedAlgorithm : public SedBase
{

protected:

	std::string   mKisaoID;


public:

	/**
	 * Creates a new SedAlgorithm with the given level, version, and package version.
	 *
	 * @param level an unsigned int, the SEDML Level to assign to this SedAlgorithm
	 *
	 * @param version an unsigned int, the SEDML Version to assign to this SedAlgorithm
	 *
	 * @param pkgVersion an unsigned int, the SEDML Sed Version to assign to this SedAlgorithm
	 */
	SedAlgorithm(unsigned int level      = SEDML_DEFAULT_LEVEL,
	             unsigned int version    = SEDML_DEFAULT_VERSION);


	/**
	 * Creates a new SedAlgorithm with the given SedNamespaces object.
	 *
	 * @param sedns the SedNamespaces object
	 */
	SedAlgorithm(SedNamespaces* sedns);


 	/**
	 * Copy constructor for SedAlgorithm.
	 *
	 * @param orig; the SedAlgorithm instance to copy.
	 */
	SedAlgorithm(const SedAlgorithm& orig);


 	/**
	 * Assignment operator for SedAlgorithm.
	 *
	 * @param rhs; the object whose values are used as the basis
	 * of the assignment
	 */
	SedAlgorithm& operator=(const SedAlgorithm& rhs);


 	/**
	 * Creates and returns a deep copy of this SedAlgorithm object.
	 *
	 * @return a (deep) copy of this SedAlgorithm object.
	 */
	virtual SedAlgorithm* clone () const;


 	/**
	 * Destructor for SedAlgorithm.
	 */
	virtual ~SedAlgorithm();


 	/**
	 * Returns the value of the "kisaoID" attribute of this SedAlgorithm.
	 *
	 * @return the value of the "kisaoID" attribute of this SedAlgorithm as a string.
	 */
	virtual const std::string& getKisaoID() const;


	/**
	 * Predicate returning @c true or @c false depending on whether this
	 * SedAlgorithm's "kisaoID" attribute has been set.
	 *
	 * @return @c true if this SedAlgorithm's "kisaoID" attribute has been set,
	 * otherwise @c false is returned.
	 */
	virtual bool isSetKisaoID() const;


	/**
	 * Sets the value of the "kisaoID" attribute of this SedAlgorithm.
	 *
	 * @param kisaoID; const std::string& value of the "kisaoID" attribute to be set
	 *
	 * @return integer value indicating success/failure of the
	 * function.  @if clike The value is drawn from the
	 * enumeration #OperationReturnValues_t. @endif The possible values
	 * returned by this function are:
	 * @li LIBSEDML_OPERATION_SUCCESS
	 * @li LIBSEDML_INVALID_ATTRIBUTE_VALUE
	 */
	virtual int setKisaoID(const std::string& kisaoID);


	/**
	 * Unsets the value of the "kisaoID" attribute of this SedAlgorithm.
	 *
	 * @return integer value indicating success/failure of the
	 * function.  @if clike The value is drawn from the
	 * enumeration #OperationReturnValues_t. @endif The possible values
	 * returned by this function are:
	 * @li LIBSEDML_OPERATION_SUCCESS
	 * @li LIBSEDML_OPERATION_FAILED
	 */
	virtual int unsetKisaoID();


	/**
	 * Returns the XML element name of this object, which for SedAlgorithm, is
	 * always @c "sedAlgorithm".
	 *
	 * @return the name of this element, i.e. @c "sedAlgorithm".
	 */
	virtual const std::string& getElementName () const;


	/**
	 * Returns the libSEDML type code for this SEDML object.
	 * 
	 * @if clike LibSEDML attaches an identifying code to every kind of SEDML
	 * object.  These are known as <em>SEDML type codes</em>.  The set of
	 * possible type codes is defined in the enumeration #SEDMLTypeCode_t.
	 * The names of the type codes all begin with the characters @c
	 * SEDML_. @endif@if java LibSEDML attaches an identifying code to every
	 * kind of SEDML object.  These are known as <em>SEDML type codes</em>.  In
	 * other languages, the set of type codes is stored in an enumeration; in
	 * the Java language interface for libSEDML, the type codes are defined as
	 * static integer constants in the interface class {@link
	 * libsbmlConstants}.  The names of the type codes all begin with the
	 * characters @c SEDML_. @endif@if python LibSEDML attaches an identifying
	 * code to every kind of SEDML object.  These are known as <em>SEDML type
	 * codes</em>.  In the Python language interface for libSEDML, the type
	 * codes are defined as static integer constants in the interface class
	 * @link libsbml@endlink.  The names of the type codes all begin with the
	 * characters @c SEDML_. @endif@if csharp LibSEDML attaches an identifying
	 * code to every kind of SEDML object.  These are known as <em>SEDML type
	 * codes</em>.  In the C# language interface for libSEDML, the type codes
	 * are defined as static integer constants in the interface class @link
	 * libsbmlcs.libsbml@endlink.  The names of the type codes all begin with
	 * the characters @c SEDML_. @endif
	 *
	 * @return the SEDML type code for this object, or
	 * @link SEDMLTypeCode_t#SEDML_UNKNOWN SEDML_UNKNOWN@endlink (default).
	 *
	 * @see getElementName()
	 */
	virtual int getTypeCode () const;


	/**
	 * Predicate returning @c true if all the required attributes
	 * for this SedAlgorithm object have been set.
	 *
	 * @note The required attributes for a SedAlgorithm object are:
	 * @li "kisaoID"
	 *
	 * @return a boolean value indicating whether all the required
	 * attributes for this object have been defined.
	 */
	virtual bool hasRequiredAttributes() const;


/** @cond doxygen-libsbml-internal */

	/**
	 * Subclasses should override this method to write out their contained
	 * SEDML objects as XML elements.  Be sure to call your parents
	 * implementation of this method as well.
	 */
	virtual void writeElements (XMLOutputStream& stream) const;


/** @endcond doxygen-libsbml-internal */


/** @cond doxygen-libsbml-internal */

	/**
	 * Accepts the given SedVisitor.
	 */
	virtual bool accept (SedVisitor& v) const;


/** @endcond doxygen-libsbml-internal */


/** @cond doxygen-libsbml-internal */

	/**
	 * Sets the parent SedDocument.
	 */
	virtual void setSedDocument (SedDocument* d);


/** @endcond doxygen-libsbml-internal */


protected:

/** @cond doxygen-libsbml-internal */

	/**
	 * Get the list of expected attributes for this element.
	 */
	virtual void addExpectedAttributes(ExpectedAttributes& attributes);


/** @endcond doxygen-libsbml-internal */


/** @cond doxygen-libsbml-internal */

	/**
	 * Read values from the given XMLAttributes set into their specific fields.
	 */
	virtual void readAttributes (const XMLAttributes& attributes,
	                             const ExpectedAttributes& expectedAttributes);


/** @endcond doxygen-libsbml-internal */


/** @cond doxygen-libsbml-internal */

	/**
	 * Write values of XMLAttributes to the output stream.
	 */
	virtual void writeAttributes (XMLOutputStream& stream) const;


/** @endcond doxygen-libsbml-internal */



};



LIBSEDML_CPP_NAMESPACE_END

#endif  /*  __cplusplus  */

#ifndef SWIG

LIBSEDML_CPP_NAMESPACE_BEGIN
BEGIN_C_DECLS

LIBSEDML_EXTERN
SedAlgorithm_t *
SedAlgorithm_create(unsigned int level, unsigned int version);


LIBSEDML_EXTERN
void
SedAlgorithm_free(SedAlgorithm_t * sa);


LIBSEDML_EXTERN
SedAlgorithm_t *
SedAlgorithm_clone(SedAlgorithm_t * sa);


LIBSEDML_EXTERN
char *
SedAlgorithm_getKisaoID(SedAlgorithm_t * sa);


LIBSEDML_EXTERN
int
SedAlgorithm_isSetKisaoID(SedAlgorithm_t * sa);


LIBSEDML_EXTERN
int
SedAlgorithm_setKisaoID(SedAlgorithm_t * sa, const char * kisaoID);


LIBSEDML_EXTERN
int
SedAlgorithm_unsetKisaoID(SedAlgorithm_t * sa);


LIBSEDML_EXTERN
int
SedAlgorithm_hasRequiredAttributes(SedAlgorithm_t * sa);




END_C_DECLS
LIBSEDML_CPP_NAMESPACE_END

#endif  /*  !SWIG  */

#endif /*  SedAlgorithm_H__  */

