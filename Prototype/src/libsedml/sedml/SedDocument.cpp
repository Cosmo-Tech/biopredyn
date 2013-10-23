/**
 * @file:   SedDocument.cpp
 * @brief:  Implementation of the SedDocument class
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


#include <sedml/SedDocument.h>
#include <sedml/SedTypes.h>
#include <sbml/xml/XMLInputStream.h>


using namespace std;


LIBSEDML_CPP_NAMESPACE_BEGIN


/*
 * Creates a new SedDocument with the given level, version, and package version.
 */
SedDocument::SedDocument (unsigned int level, unsigned int version)
	: SedBase(level, version)
	, mLevel (SEDML_INT_MAX)
	, mIsSetLevel (false)
	, mVersion (SEDML_INT_MAX)
	, mIsSetVersion (false)
	, mSimulation (level, version)
	, mModel (level, version)
	, mTask (level, version)
	, mDataGenerator (level, version)
	, mOutput (level, version)

{
	// set an SedNamespaces derived object of this package
	setSedNamespacesAndOwn(new SedNamespaces(level, version));

	// connect to child objects
	connectToChild();
}


/*
 * Creates a new SedDocument with the given SedNamespaces object.
 */
SedDocument::SedDocument (SedNamespaces* sedns)
	: SedBase(sedns)
	, mLevel (SEDML_INT_MAX)
	, mIsSetLevel (false)
	, mVersion (SEDML_INT_MAX)
	, mIsSetVersion (false)
	, mSimulation (sedns)
	, mModel (sedns)
	, mTask (sedns)
	, mDataGenerator (sedns)
	, mOutput (sedns)

{
	// set the element namespace of this object
	setElementNamespace(sedns->getURI());

	// connect to child objects
	connectToChild();
}


/*
 * Copy constructor for SedDocument.
 */
SedDocument::SedDocument (const SedDocument& orig)
	: SedBase(orig)
{
	if (&orig == NULL)
	{
		throw SedConstructorException("Null argument to copy constructor");
	}
	else
	{
		mLevel  = orig.mLevel;
		mIsSetLevel  = orig.mIsSetLevel;
		mVersion  = orig.mVersion;
		mIsSetVersion  = orig.mIsSetVersion;
		mSimulation  = orig.mSimulation;
		mModel  = orig.mModel;
		mTask  = orig.mTask;
		mDataGenerator  = orig.mDataGenerator;
		mOutput  = orig.mOutput;

		// connect to child objects
		connectToChild();
	}
}


/*
 * Assignment for SedDocument.
 */
SedDocument&
SedDocument::operator=(const SedDocument& rhs)
{
	if (&rhs == NULL)
	{
		throw SedConstructorException("Null argument to assignment");
	}
	else if (&rhs != this)
	{
		SedBase::operator=(rhs);
		mLevel  = rhs.mLevel;
		mIsSetLevel  = rhs.mIsSetLevel;
		mVersion  = rhs.mVersion;
		mIsSetVersion  = rhs.mIsSetVersion;
		mSimulation  = rhs.mSimulation;
		mModel  = rhs.mModel;
		mTask  = rhs.mTask;
		mDataGenerator  = rhs.mDataGenerator;
		mOutput  = rhs.mOutput;

		// connect to child objects
		connectToChild();
	}
	return *this;
}


/*
 * Clone for SedDocument.
 */
SedDocument*
SedDocument::clone () const
{
	return new SedDocument(*this);
}


/*
 * Destructor for SedDocument.
 */
SedDocument::~SedDocument ()
{
}


/*
 * Returns the value of the "level" attribute of this SedDocument.
 */
const int
SedDocument::getLevel() const
{
	return mLevel;
}


/*
 * Returns the value of the "version" attribute of this SedDocument.
 */
const int
SedDocument::getVersion() const
{
	return mVersion;
}


/*
 * Returns true/false if level is set.
 */
bool
SedDocument::isSetLevel() const
{
	return mIsSetLevel;
}


/*
 * Returns true/false if version is set.
 */
bool
SedDocument::isSetVersion() const
{
	return mIsSetVersion;
}


/*
 * Sets level and returns value indicating success.
 */
int
SedDocument::setLevel(int level)
{
	mLevel = level;
	mIsSetLevel = true;
	return LIBSEDML_OPERATION_SUCCESS;
}


/*
 * Sets version and returns value indicating success.
 */
int
SedDocument::setVersion(int version)
{
	mVersion = version;
	mIsSetVersion = true;
	return LIBSEDML_OPERATION_SUCCESS;
}


/*
 * Unsets level and returns value indicating success.
 */
int
SedDocument::unsetLevel()
{
	mLevel = SEDML_INT_MAX;
	mIsSetLevel = false;

	if (isSetLevel() == false)
	{
		return LIBSEDML_OPERATION_SUCCESS;
	}
	else
	{
		return LIBSEDML_OPERATION_FAILED;
	}
}


/*
 * Unsets version and returns value indicating success.
 */
int
SedDocument::unsetVersion()
{
	mVersion = SEDML_INT_MAX;
	mIsSetVersion = false;

	if (isSetVersion() == false)
	{
		return LIBSEDML_OPERATION_SUCCESS;
	}
	else
	{
		return LIBSEDML_OPERATION_FAILED;
	}
}


/*
 * Returns the  "SedListOfSimulations" in this SedDocument object.
 */
const SedListOfSimulations*
SedDocument::getListOfSimulations() const
{
	return &mSimulation;
}


/*
 * Removes the nth Simulation from the SedListOfSimulations.
 */
SedSimulation*
SedDocument::removeSimulation(unsigned int n)
{
	return mSimulation.remove(n);
}


/*
 * Removes the a Simulation with given id from the SedListOfSimulations.
 */
SedSimulation*
SedDocument::removeSimulation(const std::string& sid)
{
	return mSimulation.remove(sid);
}


/*
 * Return the nth Simulation in the SedListOfSimulations within this SedDocument.
 */
SedSimulation*
SedDocument::getSimulation(unsigned int n)
{
	return mSimulation.get(n);
}


/*
 * Return the nth Simulation in the SedListOfSimulations within this SedDocument.
 */
const SedSimulation*
SedDocument::getSimulation(unsigned int n) const
{
	return mSimulation.get(n);
}


/*
 * Return a Simulation from the SedListOfSimulations by id.
 */
SedSimulation*
SedDocument::getSimulation(const std::string& sid)
{
	return mSimulation.get(sid);
}


/*
 * Return a Simulation from the SedListOfSimulations by id.
 */
const SedSimulation*
SedDocument::getSimulation(const std::string& sid) const
{
	return mSimulation.get(sid);
}


/**
 * Adds a copy the given "SedSimulation" to this SedDocument.
 *
 * @param ss; the SedSimulation object to add
 *
 * @return integer value indicating success/failure of the
 * function.  @if clike The value is drawn from the
 * enumeration #OperationReturnValues_t. @endif The possible values
 * returned by this function are:
 * @li LIBSEDML_OPERATION_SUCCESS
 * @li LIBSEDML_INVALID_ATTRIBUTE_VALUE
 */
int
SedDocument::addSimulation(const SedSimulation* ss)
{
	if(ss == NULL) return LIBSEDML_INVALID_ATTRIBUTE_VALUE;
	mSimulation.append(ss);
	return LIBSEDML_OPERATION_SUCCESS;
}


/**
 * Get the number of SedSimulation objects in this SedDocument.
 *
 * @return the number of SedSimulation objects in this SedDocument
 */
unsigned int 
SedDocument::getNumSimulations() const
{
	return mSimulation.size();
}

/**
 * Creates a new SedUniformTimeCourse object, adds it to this SedDocuments
 * SedDocument and returns the SedUniformTimeCourse object created. 
 *
 * @return a new SedUniformTimeCourse object instance
 *
 * @see addUniformTimeCourse(const SedSimulation* ss)
 */
SedUniformTimeCourse* 
SedDocument::createUniformTimeCourse()
{
	SedUniformTimeCourse *temp = new SedUniformTimeCourse();
	if (temp != NULL) mSimulation.appendAndOwn(temp);
	return temp;
}

/*
 * Returns the  "SedListOfModels" in this SedDocument object.
 */
const SedListOfModels*
SedDocument::getListOfModels() const
{
	return &mModel;
}


/*
 * Removes the nth Model from the SedListOfModels.
 */
SedModel*
SedDocument::removeModel(unsigned int n)
{
	return mModel.remove(n);
}


/*
 * Removes the a Model with given id from the SedListOfModels.
 */
SedModel*
SedDocument::removeModel(const std::string& sid)
{
	return mModel.remove(sid);
}


/*
 * Return the nth Model in the SedListOfModels within this SedDocument.
 */
SedModel*
SedDocument::getModel(unsigned int n)
{
	return mModel.get(n);
}


/*
 * Return the nth Model in the SedListOfModels within this SedDocument.
 */
const SedModel*
SedDocument::getModel(unsigned int n) const
{
	return mModel.get(n);
}


/*
 * Return a Model from the SedListOfModels by id.
 */
SedModel*
SedDocument::getModel(const std::string& sid)
{
	return mModel.get(sid);
}


/*
 * Return a Model from the SedListOfModels by id.
 */
const SedModel*
SedDocument::getModel(const std::string& sid) const
{
	return mModel.get(sid);
}


/**
 * Adds a copy the given "SedModel" to this SedDocument.
 *
 * @param sm; the SedModel object to add
 *
 * @return integer value indicating success/failure of the
 * function.  @if clike The value is drawn from the
 * enumeration #OperationReturnValues_t. @endif The possible values
 * returned by this function are:
 * @li LIBSEDML_OPERATION_SUCCESS
 * @li LIBSEDML_INVALID_ATTRIBUTE_VALUE
 */
int
SedDocument::addModel(const SedModel* sm)
{
	if(sm == NULL) return LIBSEDML_INVALID_ATTRIBUTE_VALUE;
	mModel.append(sm);
	return LIBSEDML_OPERATION_SUCCESS;
}


/**
 * Get the number of SedModel objects in this SedDocument.
 *
 * @return the number of SedModel objects in this SedDocument
 */
unsigned int 
SedDocument::getNumModels() const
{
	return mModel.size();
}

/**
 * Creates a new SedModel object, adds it to this SedDocuments
 * SedDocument and returns the SedModel object created. 
 *
 * @return a new SedModel object instance
 *
 * @see addSedModel(const SedModel* sm)
 */
SedModel* 
SedDocument::createModel()
{
	SedModel *temp = new SedModel();
	if (temp != NULL) mModel.appendAndOwn(temp);
	return temp;
}

/*
 * Returns the  "SedListOfTasks" in this SedDocument object.
 */
const SedListOfTasks*
SedDocument::getListOfTasks() const
{
	return &mTask;
}


/*
 * Removes the nth Task from the SedListOfTasks.
 */
SedTask*
SedDocument::removeTask(unsigned int n)
{
	return mTask.remove(n);
}


/*
 * Removes the a Task with given id from the SedListOfTasks.
 */
SedTask*
SedDocument::removeTask(const std::string& sid)
{
	return mTask.remove(sid);
}


/*
 * Return the nth Task in the SedListOfTasks within this SedDocument.
 */
SedTask*
SedDocument::getTask(unsigned int n)
{
	return mTask.get(n);
}


/*
 * Return the nth Task in the SedListOfTasks within this SedDocument.
 */
const SedTask*
SedDocument::getTask(unsigned int n) const
{
	return mTask.get(n);
}


/*
 * Return a Task from the SedListOfTasks by id.
 */
SedTask*
SedDocument::getTask(const std::string& sid)
{
	return mTask.get(sid);
}


/*
 * Return a Task from the SedListOfTasks by id.
 */
const SedTask*
SedDocument::getTask(const std::string& sid) const
{
	return mTask.get(sid);
}


/**
 * Adds a copy the given "SedTask" to this SedDocument.
 *
 * @param st; the SedTask object to add
 *
 * @return integer value indicating success/failure of the
 * function.  @if clike The value is drawn from the
 * enumeration #OperationReturnValues_t. @endif The possible values
 * returned by this function are:
 * @li LIBSEDML_OPERATION_SUCCESS
 * @li LIBSEDML_INVALID_ATTRIBUTE_VALUE
 */
int
SedDocument::addTask(const SedTask* st)
{
	if(st == NULL) return LIBSEDML_INVALID_ATTRIBUTE_VALUE;
	mTask.append(st);
	return LIBSEDML_OPERATION_SUCCESS;
}


/**
 * Get the number of SedTask objects in this SedDocument.
 *
 * @return the number of SedTask objects in this SedDocument
 */
unsigned int 
SedDocument::getNumTasks() const
{
	return mTask.size();
}

/**
 * Creates a new SedTask object, adds it to this SedDocuments
 * SedDocument and returns the SedTask object created. 
 *
 * @return a new SedTask object instance
 *
 * @see addSedTask(const SedTask* st)
 */
SedTask* 
SedDocument::createTask()
{
	SedTask *temp = new SedTask();
	if (temp != NULL) mTask.appendAndOwn(temp);
	return temp;
}

/*
 * Returns the  "SedListOfDataGenerators" in this SedDocument object.
 */
const SedListOfDataGenerators*
SedDocument::getListOfDataGenerators() const
{
	return &mDataGenerator;
}


/*
 * Removes the nth DataGenerator from the SedListOfDataGenerators.
 */
SedDataGenerator*
SedDocument::removeDataGenerator(unsigned int n)
{
	return mDataGenerator.remove(n);
}


/*
 * Removes the a DataGenerator with given id from the SedListOfDataGenerators.
 */
SedDataGenerator*
SedDocument::removeDataGenerator(const std::string& sid)
{
	return mDataGenerator.remove(sid);
}


/*
 * Return the nth DataGenerator in the SedListOfDataGenerators within this SedDocument.
 */
SedDataGenerator*
SedDocument::getDataGenerator(unsigned int n)
{
	return mDataGenerator.get(n);
}


/*
 * Return the nth DataGenerator in the SedListOfDataGenerators within this SedDocument.
 */
const SedDataGenerator*
SedDocument::getDataGenerator(unsigned int n) const
{
	return mDataGenerator.get(n);
}


/*
 * Return a DataGenerator from the SedListOfDataGenerators by id.
 */
SedDataGenerator*
SedDocument::getDataGenerator(const std::string& sid)
{
	return mDataGenerator.get(sid);
}


/*
 * Return a DataGenerator from the SedListOfDataGenerators by id.
 */
const SedDataGenerator*
SedDocument::getDataGenerator(const std::string& sid) const
{
	return mDataGenerator.get(sid);
}


/**
 * Adds a copy the given "SedDataGenerator" to this SedDocument.
 *
 * @param sdg; the SedDataGenerator object to add
 *
 * @return integer value indicating success/failure of the
 * function.  @if clike The value is drawn from the
 * enumeration #OperationReturnValues_t. @endif The possible values
 * returned by this function are:
 * @li LIBSEDML_OPERATION_SUCCESS
 * @li LIBSEDML_INVALID_ATTRIBUTE_VALUE
 */
int
SedDocument::addDataGenerator(const SedDataGenerator* sdg)
{
	if(sdg == NULL) return LIBSEDML_INVALID_ATTRIBUTE_VALUE;
	mDataGenerator.append(sdg);
	return LIBSEDML_OPERATION_SUCCESS;
}


/**
 * Get the number of SedDataGenerator objects in this SedDocument.
 *
 * @return the number of SedDataGenerator objects in this SedDocument
 */
unsigned int 
SedDocument::getNumDataGenerators() const
{
	return mDataGenerator.size();
}

/**
 * Creates a new SedDataGenerator object, adds it to this SedDocuments
 * SedDocument and returns the SedDataGenerator object created. 
 *
 * @return a new SedDataGenerator object instance
 *
 * @see addSedDataGenerator(const SedDataGenerator* sdg)
 */
SedDataGenerator* 
SedDocument::createDataGenerator()
{
	SedDataGenerator *temp = new SedDataGenerator();
	if (temp != NULL) mDataGenerator.appendAndOwn(temp);
	return temp;
}

/*
 * Returns the  "SedListOfOutputs" in this SedDocument object.
 */
const SedListOfOutputs*
SedDocument::getListOfOutputs() const
{
	return &mOutput;
}


/*
 * Removes the nth Output from the SedListOfOutputs.
 */
SedOutput*
SedDocument::removeOutput(unsigned int n)
{
	return mOutput.remove(n);
}


/*
 * Removes the a Output with given id from the SedListOfOutputs.
 */
SedOutput*
SedDocument::removeOutput(const std::string& sid)
{
	return mOutput.remove(sid);
}


/*
 * Return the nth Output in the SedListOfOutputs within this SedDocument.
 */
SedOutput*
SedDocument::getOutput(unsigned int n)
{
	return mOutput.get(n);
}


/*
 * Return the nth Output in the SedListOfOutputs within this SedDocument.
 */
const SedOutput*
SedDocument::getOutput(unsigned int n) const
{
	return mOutput.get(n);
}


/*
 * Return a Output from the SedListOfOutputs by id.
 */
SedOutput*
SedDocument::getOutput(const std::string& sid)
{
	return mOutput.get(sid);
}


/*
 * Return a Output from the SedListOfOutputs by id.
 */
const SedOutput*
SedDocument::getOutput(const std::string& sid) const
{
	return mOutput.get(sid);
}


/**
 * Adds a copy the given "SedOutput" to this SedDocument.
 *
 * @param so; the SedOutput object to add
 *
 * @return integer value indicating success/failure of the
 * function.  @if clike The value is drawn from the
 * enumeration #OperationReturnValues_t. @endif The possible values
 * returned by this function are:
 * @li LIBSEDML_OPERATION_SUCCESS
 * @li LIBSEDML_INVALID_ATTRIBUTE_VALUE
 */
int
SedDocument::addOutput(const SedOutput* so)
{
	if(so == NULL) return LIBSEDML_INVALID_ATTRIBUTE_VALUE;
	mOutput.append(so);
	return LIBSEDML_OPERATION_SUCCESS;
}


/**
 * Get the number of SedOutput objects in this SedDocument.
 *
 * @return the number of SedOutput objects in this SedDocument
 */
unsigned int 
SedDocument::getNumOutputs() const
{
	return mOutput.size();
}

/**
 * Creates a new SedReport object, adds it to this SedDocuments
 * SedDocument and returns the SedReport object created. 
 *
 * @return a new SedReport object instance
 *
 * @see addReport(const SedOutput* so)
 */
SedReport* 
SedDocument::createReport()
{
	SedReport *temp = new SedReport();
	if (temp != NULL) mOutput.appendAndOwn(temp);
	return temp;
}

/**
 * Creates a new SedPlot2D object, adds it to this SedDocuments
 * SedDocument and returns the SedPlot2D object created. 
 *
 * @return a new SedPlot2D object instance
 *
 * @see addPlot2D(const SedOutput* so)
 */
SedPlot2D* 
SedDocument::createPlot2D()
{
	SedPlot2D *temp = new SedPlot2D();
	if (temp != NULL) mOutput.appendAndOwn(temp);
	return temp;
}

/**
 * Creates a new SedPlot3D object, adds it to this SedDocuments
 * SedDocument and returns the SedPlot3D object created. 
 *
 * @return a new SedPlot3D object instance
 *
 * @see addPlot3D(const SedOutput* so)
 */
SedPlot3D* 
SedDocument::createPlot3D()
{
	SedPlot3D *temp = new SedPlot3D();
	if (temp != NULL) mOutput.appendAndOwn(temp);
	return temp;
}

/*
 * Returns the XML element name of this object
 */
const std::string&
SedDocument::getElementName () const
{
	static const string name = "sedML";
	return name;
}


/**
 * return the SEDML object corresponding to next XMLToken.
 */
SedBase*
SedDocument::createObject(XMLInputStream& stream)
{
	SedBase* object = NULL;

	const string& name   = stream.peek().getName();

	SedBase::connectToChild();

	if (name == "listOfSimulations")
	{
		object = &mSimulation;
	}

	if (name == "listOfModels")
	{
		object = &mModel;
	}

	if (name == "listOfTasks")
	{
		object = &mTask;
	}

	if (name == "listOfDataGenerators")
	{
		object = &mDataGenerator;
	}

	if (name == "listOfOutputs")
	{
		object = &mOutput;
	}

	return object;
}


/*
 * Read values from the given XMLAttributes set into their specific fields.
 */
void
SedDocument::connectToChild ()
{
	SedBase::connectToChild();

	mSimulation.connectToParent(this);
	mModel.connectToParent(this);
	mTask.connectToParent(this);
	mDataGenerator.connectToParent(this);
	mOutput.connectToParent(this);
}


/*
 * Returns the libSEDML type code for this SEDML object.
 */
int
SedDocument::getTypeCode () const
{
	return SEDML_DOCUMENT;
}


/*
 * check if all the required attributes are set
 */
bool
SedDocument::hasRequiredAttributes () const
{
	bool allPresent = true;

	if (isSetLevel() == false)
		allPresent = false;

	if (isSetVersion() == false)
		allPresent = false;

	return allPresent;
}


/*
 * check if all the required elements are set
 */
bool
SedDocument::hasRequiredElements () const
{
	bool allPresent = true;

	return allPresent;
}


/** @cond doxygen-libsbml-internal */

/*
 * write contained elements
 */
void
SedDocument::writeElements (XMLOutputStream& stream) const
{
	SedBase::writeElements(stream);
	if (getNumSimulations() > 0)
	{
		mSimulation.write(stream);
	}
	if (getNumModels() > 0)
	{
		mModel.write(stream);
	}
	if (getNumTasks() > 0)
	{
		mTask.write(stream);
	}
	if (getNumDataGenerators() > 0)
	{
		mDataGenerator.write(stream);
	}
	if (getNumOutputs() > 0)
	{
		mOutput.write(stream);
	}
}


/** @endcond doxygen-libsbml-internal */


/** @cond doxygen-libsbml-internal */

/*
 * Accepts the given SedVisitor.
 */
bool
SedDocument::accept (SedVisitor& v) const
{
	return false;

}


/** @endcond doxygen-libsbml-internal */


/** @cond doxygen-libsbml-internal */

/*
 * Sets the parent SedDocument.
 */
void
SedDocument::setSedDocument (SedDocument* d)
{
	SedBase::setSedDocument(d);
}


/** @endcond doxygen-libsbml-internal */


/** @cond doxygen-libsbml-internal */

/*
 * Get the list of expected attributes for this element.
 */
void
SedDocument::addExpectedAttributes(ExpectedAttributes& attributes)
{
	SedBase::addExpectedAttributes(attributes);

	attributes.add("level");
	attributes.add("version");
}


/** @endcond doxygen-libsbml-internal */


/** @cond doxygen-libsbml-internal */

/*
 * Read values from the given XMLAttributes set into their specific fields.
 */
void
SedDocument::readAttributes (const XMLAttributes& attributes,
                             const ExpectedAttributes& expectedAttributes)
{
	SedBase::readAttributes(attributes, expectedAttributes);

	bool assigned = false;

	//
	// level int   ( use = "required" )
	//
	mIsSetLevel = attributes.readInto("level", mLevel, getErrorLog(), true);

	//
	// version int   ( use = "required" )
	//
	mIsSetVersion = attributes.readInto("version", mVersion, getErrorLog(), true);

}


/** @endcond doxygen-libsbml-internal */


/** @cond doxygen-libsbml-internal */

/*
 * Write values of XMLAttributes to the output stream.
 */
	void
SedDocument::writeAttributes (XMLOutputStream& stream) const
{
	SedBase::writeAttributes(stream);

	if (isSetLevel() == true)
		stream.writeAttribute("level", getPrefix(), mLevel);

	if (isSetVersion() == true)
		stream.writeAttribute("version", getPrefix(), mVersion);

}


/** @endcond doxygen-libsbml-internal */




/*
 * @return the nth error encountered during the parse of this
 * SedDocument or @c NULL if n > getNumErrors() - 1.
 */
const SedError*
SedDocument::getError (unsigned int n) const
{
  return mErrorLog.getError(n);
}


/*
 * @return the number of errors encountered during the parse of this
 * SedDocument.
 */
unsigned int
SedDocument::getNumErrors () const
{
  return mErrorLog.getNumErrors();
}


unsigned int 
SedDocument::getNumErrors (unsigned int severity) const
{
  return getErrorLog()->getNumFailsWithSeverity(severity);
}


/*
 * @return the SedErrorLog used to log errors during while reading and
 * validating Sed.
 */
SedErrorLog*
SedDocument::getErrorLog ()
{
  return &mErrorLog;
}


/*
 * @return the SedErrorLog used to log errors during while reading and
 * validating Sed.
 */
const SedErrorLog*
SedDocument::getErrorLog () const
{
  return &mErrorLog;
}

/*
 *
 * Subclasses should override this method to write their xmlns attriubutes
 * (if any) to the XMLOutputStream.  Be sure to call your parents implementation
 * of this method as well.
 *
 */
void
SedDocument::writeXMLNS (XMLOutputStream& stream) const
{
  // need to check that we have indeed a namespace set!
  XMLNamespaces * thisNs = this->getNamespaces();

  // the sbml namespace is missing - add it
  if (thisNs == NULL)
  {
    XMLNamespaces xmlns;
    xmlns.add(SEDML_XMLNS_L1);

    mSedNamespaces->setNamespaces(&xmlns);
    thisNs = getNamespaces();
  }
  else if (thisNs->getLength() == 0)
  {
     thisNs->add(SEDML_XMLNS_L1);
  }
  else
  {
    // check that there is an sbml namespace
    std::string sedmlURI = SedNamespaces::getSedNamespaceURI(mLevel, mVersion);
    std::string sedmlPrefix = thisNs->getPrefix(sedmlURI);
    if (thisNs->hasNS(sedmlURI, sedmlPrefix) == false)
    {
      // the sbml ns is not present
      std::string other = thisNs->getURI(sedmlPrefix);
      if (other.empty() == false)
      {
        // there is another ns with the prefix that the sbml ns expects to have
        //remove the this ns, add the sbml ns and 
        //add the new ns with a new prefix
        thisNs->remove(sedmlPrefix);
        thisNs->add(sedmlURI, sedmlPrefix);
        thisNs->add(other, "addedPrefix");
      }
      else
      {
        thisNs->add(sedmlURI, sedmlPrefix);
      }
    }
  }

  XMLNamespaces * xmlns = thisNs->clone();
  if (xmlns != NULL) 
  {
    stream << *(xmlns);
    delete xmlns;
  }
}

/*
  * @return the Namespaces associated with this SBML object
  */
XMLNamespaces* 
SedDocument::getNamespaces() const
{
  return mSedNamespaces->getNamespaces();
}/**
 * write comments
 */
LIBSEDML_EXTERN
SedDocument_t *
SedDocument_create(unsigned int level, unsigned int version)
{
	return new SedDocument(level, version);
}


/**
 * write comments
 */
LIBSEDML_EXTERN
void
SedDocument_free(SedDocument_t * sd)
{
	if (sd != NULL)
		delete sd;
}


/**
 * write comments
 */
LIBSEDML_EXTERN
SedDocument_t *
SedDocument_clone(SedDocument_t * sd)
{
	if (sd != NULL)
	{
		return static_cast<SedDocument_t*>(sd->clone());
	}
	else
	{
		return NULL;
	}
}


/**
 * write comments
 */
LIBSEDML_EXTERN
int
SedDocument_getLevel(SedDocument_t * sd)
{
	return (sd != NULL) ? sd->getLevel() : SEDML_INT_MAX;
}


/**
 * write comments
 */
LIBSEDML_EXTERN
int
SedDocument_getVersion(SedDocument_t * sd)
{
	return (sd != NULL) ? sd->getVersion() : SEDML_INT_MAX;
}


/**
 * write comments
 */
LIBSEDML_EXTERN
int
SedDocument_isSetLevel(SedDocument_t * sd)
{
	return (sd != NULL) ? static_cast<int>(sd->isSetLevel()) : 0;
}


/**
 * write comments
 */
LIBSEDML_EXTERN
int
SedDocument_isSetVersion(SedDocument_t * sd)
{
	return (sd != NULL) ? static_cast<int>(sd->isSetVersion()) : 0;
}


/**
 * write comments
 */
LIBSEDML_EXTERN
int
SedDocument_setLevel(SedDocument_t * sd, int level)
{
	return (sd != NULL) ? sd->setLevel(level) : LIBSEDML_INVALID_OBJECT;
}


/**
 * write comments
 */
LIBSEDML_EXTERN
int
SedDocument_setVersion(SedDocument_t * sd, int version)
{
	return (sd != NULL) ? sd->setVersion(version) : LIBSEDML_INVALID_OBJECT;
}


/**
 * write comments
 */
LIBSEDML_EXTERN
int
SedDocument_unsetLevel(SedDocument_t * sd)
{
	return (sd != NULL) ? sd->unsetLevel() : LIBSEDML_INVALID_OBJECT;
}


/**
 * write comments
 */
LIBSEDML_EXTERN
int
SedDocument_unsetVersion(SedDocument_t * sd)
{
	return (sd != NULL) ? sd->unsetVersion() : LIBSEDML_INVALID_OBJECT;
}


LIBSEDML_EXTERN
int
SedDocument_addSimulation(SedDocument_t * sd, SedSimulation_t * ss)
{
	return  (sd != NULL) ? sd->addSimulation(ss) : LIBSBML_INVALID_OBJECT;
}

LIBSEDML_EXTERN
SedUniformTimeCourse_t *
SedDocument_createUniformTimeCourse(SedDocument_t * sd)
{
	return  (sd != NULL) ? sd->createUniformTimeCourse() : NULL;
}

LIBSEDML_EXTERN
SedListOf_t *
SedDocument_getSedListOfSimulations(SedDocument_t * sd)
{
	return  (sd != NULL) ? (SedListOf_t *)sd->getListOfSimulations() : NULL;
}

LIBSEDML_EXTERN
SedSimulation_t *
SedDocument_getSimulation(SedDocument_t * sd, unsigned int n)
{
	return  (sd != NULL) ? sd->getSimulation(n) : NULL;
}

LIBSEDML_EXTERN
SedSimulation_t *
SedDocument_getSimulationById(SedDocument_t * sd, const char * sid)
{
	return  (sd != NULL) ? sd->getSimulation(sid) : NULL;
}

LIBSEDML_EXTERN
unsigned int
SedDocument_getNumSimulations(SedDocument_t * sd)
{
	return  (sd != NULL) ? sd->getNumSimulations() : SEDML_INT_MAX;
}

LIBSEDML_EXTERN
SedSimulation_t *
SedDocument_removeSimulation(SedDocument_t * sd, unsigned int n)
{
	return  (sd != NULL) ? sd->removeSimulation(n) : NULL;
}

LIBSEDML_EXTERN
SedSimulation_t *
SedDocument_removeSimulationById(SedDocument_t * sd, const char * sid)
{
	return  (sd != NULL) ? sd->removeSimulation(sid) : NULL;
}

LIBSEDML_EXTERN
int
SedDocument_addModel(SedDocument_t * sd, SedModel_t * sm)
{
	return  (sd != NULL) ? sd->addModel(sm) : LIBSBML_INVALID_OBJECT;
}

LIBSEDML_EXTERN
SedModel_t *
SedDocument_createModel(SedDocument_t * sd)
{
	return  (sd != NULL) ? sd->createModel() : NULL;
}

LIBSEDML_EXTERN
SedListOf_t *
SedDocument_getSedListOfModels(SedDocument_t * sd)
{
	return  (sd != NULL) ? (SedListOf_t *)sd->getListOfModels() : NULL;
}

LIBSEDML_EXTERN
SedModel_t *
SedDocument_getModel(SedDocument_t * sd, unsigned int n)
{
	return  (sd != NULL) ? sd->getModel(n) : NULL;
}

LIBSEDML_EXTERN
SedModel_t *
SedDocument_getModelById(SedDocument_t * sd, const char * sid)
{
	return  (sd != NULL) ? sd->getModel(sid) : NULL;
}

LIBSEDML_EXTERN
unsigned int
SedDocument_getNumModels(SedDocument_t * sd)
{
	return  (sd != NULL) ? sd->getNumModels() : SEDML_INT_MAX;
}

LIBSEDML_EXTERN
SedModel_t *
SedDocument_removeModel(SedDocument_t * sd, unsigned int n)
{
	return  (sd != NULL) ? sd->removeModel(n) : NULL;
}

LIBSEDML_EXTERN
SedModel_t *
SedDocument_removeModelById(SedDocument_t * sd, const char * sid)
{
	return  (sd != NULL) ? sd->removeModel(sid) : NULL;
}

LIBSEDML_EXTERN
int
SedDocument_addTask(SedDocument_t * sd, SedTask_t * st)
{
	return  (sd != NULL) ? sd->addTask(st) : LIBSBML_INVALID_OBJECT;
}

LIBSEDML_EXTERN
SedTask_t *
SedDocument_createTask(SedDocument_t * sd)
{
	return  (sd != NULL) ? sd->createTask() : NULL;
}

LIBSEDML_EXTERN
SedListOf_t *
SedDocument_getSedListOfTasks(SedDocument_t * sd)
{
	return  (sd != NULL) ? (SedListOf_t *)sd->getListOfTasks() : NULL;
}

LIBSEDML_EXTERN
SedTask_t *
SedDocument_getTask(SedDocument_t * sd, unsigned int n)
{
	return  (sd != NULL) ? sd->getTask(n) : NULL;
}

LIBSEDML_EXTERN
SedTask_t *
SedDocument_getTaskById(SedDocument_t * sd, const char * sid)
{
	return  (sd != NULL) ? sd->getTask(sid) : NULL;
}

LIBSEDML_EXTERN
unsigned int
SedDocument_getNumTasks(SedDocument_t * sd)
{
	return  (sd != NULL) ? sd->getNumTasks() : SEDML_INT_MAX;
}

LIBSEDML_EXTERN
SedTask_t *
SedDocument_removeTask(SedDocument_t * sd, unsigned int n)
{
	return  (sd != NULL) ? sd->removeTask(n) : NULL;
}

LIBSEDML_EXTERN
SedTask_t *
SedDocument_removeTaskById(SedDocument_t * sd, const char * sid)
{
	return  (sd != NULL) ? sd->removeTask(sid) : NULL;
}

LIBSEDML_EXTERN
int
SedDocument_addDataGenerator(SedDocument_t * sd, SedDataGenerator_t * sdg)
{
	return  (sd != NULL) ? sd->addDataGenerator(sdg) : LIBSBML_INVALID_OBJECT;
}

LIBSEDML_EXTERN
SedDataGenerator_t *
SedDocument_createDataGenerator(SedDocument_t * sd)
{
	return  (sd != NULL) ? sd->createDataGenerator() : NULL;
}

LIBSEDML_EXTERN
SedListOf_t *
SedDocument_getSedListOfDataGenerators(SedDocument_t * sd)
{
	return  (sd != NULL) ? (SedListOf_t *)sd->getListOfDataGenerators() : NULL;
}

LIBSEDML_EXTERN
SedDataGenerator_t *
SedDocument_getDataGenerator(SedDocument_t * sd, unsigned int n)
{
	return  (sd != NULL) ? sd->getDataGenerator(n) : NULL;
}

LIBSEDML_EXTERN
SedDataGenerator_t *
SedDocument_getDataGeneratorById(SedDocument_t * sd, const char * sid)
{
	return  (sd != NULL) ? sd->getDataGenerator(sid) : NULL;
}

LIBSEDML_EXTERN
unsigned int
SedDocument_getNumDataGenerators(SedDocument_t * sd)
{
	return  (sd != NULL) ? sd->getNumDataGenerators() : SEDML_INT_MAX;
}

LIBSEDML_EXTERN
SedDataGenerator_t *
SedDocument_removeDataGenerator(SedDocument_t * sd, unsigned int n)
{
	return  (sd != NULL) ? sd->removeDataGenerator(n) : NULL;
}

LIBSEDML_EXTERN
SedDataGenerator_t *
SedDocument_removeDataGeneratorById(SedDocument_t * sd, const char * sid)
{
	return  (sd != NULL) ? sd->removeDataGenerator(sid) : NULL;
}

LIBSEDML_EXTERN
int
SedDocument_addOutput(SedDocument_t * sd, SedOutput_t * so)
{
	return  (sd != NULL) ? sd->addOutput(so) : LIBSBML_INVALID_OBJECT;
}

LIBSEDML_EXTERN
SedReport_t *
SedDocument_createReport(SedDocument_t * sd)
{
	return  (sd != NULL) ? sd->createReport() : NULL;
}

LIBSEDML_EXTERN
SedPlot2D_t *
SedDocument_createPlot2D(SedDocument_t * sd)
{
	return  (sd != NULL) ? sd->createPlot2D() : NULL;
}

LIBSEDML_EXTERN
SedPlot3D_t *
SedDocument_createPlot3D(SedDocument_t * sd)
{
	return  (sd != NULL) ? sd->createPlot3D() : NULL;
}

LIBSEDML_EXTERN
SedListOf_t *
SedDocument_getSedListOfOutputs(SedDocument_t * sd)
{
	return  (sd != NULL) ? (SedListOf_t *)sd->getListOfOutputs() : NULL;
}

LIBSEDML_EXTERN
SedOutput_t *
SedDocument_getOutput(SedDocument_t * sd, unsigned int n)
{
	return  (sd != NULL) ? sd->getOutput(n) : NULL;
}

LIBSEDML_EXTERN
SedOutput_t *
SedDocument_getOutputById(SedDocument_t * sd, const char * sid)
{
	return  (sd != NULL) ? sd->getOutput(sid) : NULL;
}

LIBSEDML_EXTERN
unsigned int
SedDocument_getNumOutputs(SedDocument_t * sd)
{
	return  (sd != NULL) ? sd->getNumOutputs() : SEDML_INT_MAX;
}

LIBSEDML_EXTERN
SedOutput_t *
SedDocument_removeOutput(SedDocument_t * sd, unsigned int n)
{
	return  (sd != NULL) ? sd->removeOutput(n) : NULL;
}

LIBSEDML_EXTERN
SedOutput_t *
SedDocument_removeOutputById(SedDocument_t * sd, const char * sid)
{
	return  (sd != NULL) ? sd->removeOutput(sid) : NULL;
}

/**
 * write comments
 */
LIBSEDML_EXTERN
int
SedDocument_hasRequiredAttributes(SedDocument_t * sd)
{
	return (sd != NULL) ? static_cast<int>(sd->hasRequiredAttributes()) : 0;
}


/**
 * write comments
 */
LIBSEDML_EXTERN
int
SedDocument_hasRequiredElements(SedDocument_t * sd)
{
	return (sd != NULL) ? static_cast<int>(sd->hasRequiredElements()) : 0;
}




LIBSEDML_CPP_NAMESPACE_END


