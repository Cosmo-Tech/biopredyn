/* ----------------------------------------------------------------------------
 * This file was automatically generated by SWIG (http://www.swig.org).
 * Version 2.0.6
 *
 * Do not make changes to this file unless you know what you are doing--modify
 * the SWIG interface file instead.
 * ----------------------------------------------------------------------------- */

package org.sbml.libsbml;

/** 
 * 
 * Representation of a qualified XML name.
 * <p>
 * <p style='color: #777; font-style: italic'>
This class of objects is defined by libSBML only and has no direct
equivalent in terms of SBML components.  This class is not prescribed by
the SBML specifications, although it is used to implement features
defined in SBML.
</p>

 * <p>
 * A 'triple' in the libSBML XML layer encapsulates the notion of qualified
 * name, meaning an element name or an attribute name with an optional
 * namespace qualifier.  An {@link XMLTriple} instance carries up to three data items:
 * <p>
 * <ul>
 * <p>
 * <li> The name of the attribute or element; that is, the attribute name
 * as it appears in an XML document or data stream;
 * <p>
 * <li> The XML namespace prefix (if any) of the attribute.  For example,
 * in the following fragment of XML, the namespace prefix is the string
 * <code>mysim</code> and it appears on both the element
 * <code>someelement</code> and the attribute <code>attribA</code>.  When
 * both the element and the attribute are stored as {@link XMLTriple} objects,
 * their <i>prefix</i> is <code>mysim</code>.
 * <div class='fragment'><pre>
&lt;mysim:someelement mysim:attribA='value' /&gt;
</pre></div>
 * <p>
 * <li> The XML namespace URI with which the prefix is associated.  In
 * XML, every namespace used must be declared and mapped to a URI.
 * <p>
 * </ul>
 * <p>
 * {@link XMLTriple} objects are the lowest-level data item in the XML layer
 * of libSBML.  Other objects such as {@link XMLToken} make use of {@link XMLTriple}
 * objects.
 */

public class XMLTriple {
   private long swigCPtr;
   protected boolean swigCMemOwn;

   protected XMLTriple(long cPtr, boolean cMemoryOwn)
   {
     swigCMemOwn = cMemoryOwn;
     swigCPtr    = cPtr;
   }

   protected static long getCPtr(XMLTriple obj)
   {
     return (obj == null) ? 0 : obj.swigCPtr;
   }

   protected static long getCPtrAndDisown (XMLTriple obj)
   {
     long ptr = 0;

     if (obj != null)
     {
       ptr             = obj.swigCPtr;
       obj.swigCMemOwn = false;
     }

     return ptr;
   }

  protected void finalize() {
    delete();
  }

  public synchronized void delete() {
    if (swigCPtr != 0) {
      if (swigCMemOwn) {
        swigCMemOwn = false;
        libsbmlJNI.delete_XMLTriple(swigCPtr);
      }
      swigCPtr = 0;
    }
  }

  /**
   * Equality comparison method for XMLTriple.
   * <p>
   * Because the Java methods for libSBML are actually wrappers around code
   * implemented in C++ and C, certain operations will not behave as
   * expected.  Equality comparison is one such case.  An instance of a
   * libSBML object class is actually a <em>proxy object</em>
   * wrapping the real underlying C/C++ object.  The normal <code>==</code>
   * equality operator in Java will <em>only compare the Java proxy objects</em>,
   * not the underlying native object.  The result is almost never what you
   * want in practical situations.  Unfortunately, Java does not provide a
   * way to override <code>==</code>.
   *  <p>
   * The alternative that must be followed is to use the
   * <code>equals()</code> method.  The <code>equals</code> method on this
   * class overrides the default java.lang.Object one, and performs an
   * intelligent comparison of instances of objects of this class.  The
   * result is an assessment of whether two libSBML Java objects are truly 
   * the same underlying native-code objects.
   *  <p>
   * The use of this method in practice is the same as the use of any other
   * Java <code>equals</code> method.  For example,
   * <em>a</em><code>.equals(</code><em>b</em><code>)</code> returns
   * <code>true</code> if <em>a</em> and <em>b</em> are references to the
   * same underlying object.
   *
   * @param sb a reference to an object to which the current object
   * instance will be compared
   *
   * @return <code>true</code> if <code>sb</code> refers to the same underlying 
   * native object as this one, <code>false</code> otherwise
   */
  public boolean equals(Object sb)
  {
    if ( this == sb ) 
    {
      return true;
    }
    return swigCPtr == getCPtr((XMLTriple)(sb));
  }

  /**
   * Returns a hashcode for this XMLTriple object.
   *
   * @return a hash code usable by Java methods that need them.
   */
  public int hashCode()
  {
    return (int)(swigCPtr^(swigCPtr>>>32));
  }

  
/**
   * Creates a new, empty {@link XMLTriple}.
   */ public
 XMLTriple() {
    this(libsbmlJNI.new_XMLTriple__SWIG_0(), true);
  }

  
/**
   * Creates a new {@link XMLTriple} with the given <code>name</code>, <code>uri</code> and and 
   * <code>prefix</code>.
   * <p>
   * @param name a string, name for the {@link XMLTriple}.
   * @param uri a string, URI of the {@link XMLTriple}.
   * @param prefix a string, prefix for the URI of the {@link XMLTriple},
   * <p>
   * @throws XMLConstructorException 
   * Thrown if the argument <code>orig</code> is <code>null.</code>
   */ public
 XMLTriple(String name, String uri, String prefix) {
    this(libsbmlJNI.new_XMLTriple__SWIG_1(name, uri, prefix), true);
  }

  
/**
   * Creates a new {@link XMLTriple} by splitting the given <code>triplet</code> on the
   * separator character <code>sepchar</code>.
   * <p>
   * Triplet may be in one of the following formats:
   * <ul>
   * <li> name
   * <li> URI sepchar name
   * <li> URI sepchar name sepchar prefix
   * </ul>
   * @param triplet a string representing the triplet as above
   * @param sepchar a character, the sepchar used in the triplet
   * <p>
   * @throws XMLConstructorException 
   * Thrown if the argument <code>orig</code> is <code>null.</code>
   * <p>
   * <!-- Don't remove the leading </dl> below. It's a hack for javadoc. -->
</dl><dl class='docnote'><dt><b>Documentation note:</b></dt><dd>
The native C++ implementation of this method defines a default argument
value. In the documentation generated for different libSBML language
bindings, you may or may not see corresponding arguments in the method
declarations. For example, in Java and C#, a default argument is handled by
declaring two separate methods, with one of them having the argument and
the other one lacking the argument. However, the libSBML documentation will
be <em>identical</em> for both methods. Consequently, if you are reading
this and do not see an argument even though one is described, please look
for descriptions of other variants of this method near where this one
appears in the documentation.
</dd></dl>
 
   */ public
 XMLTriple(String triplet, char sepchar) {
    this(libsbmlJNI.new_XMLTriple__SWIG_2(triplet, sepchar), true);
  }

  
/**
   * Creates a new {@link XMLTriple} by splitting the given <code>triplet</code> on the
   * separator character <code>sepchar</code>.
   * <p>
   * Triplet may be in one of the following formats:
   * <ul>
   * <li> name
   * <li> URI sepchar name
   * <li> URI sepchar name sepchar prefix
   * </ul>
   * @param triplet a string representing the triplet as above
   * @param sepchar a character, the sepchar used in the triplet
   * <p>
   * @throws XMLConstructorException 
   * Thrown if the argument <code>orig</code> is <code>null.</code>
   * <p>
   * <!-- Don't remove the leading </dl> below. It's a hack for javadoc. -->
</dl><dl class='docnote'><dt><b>Documentation note:</b></dt><dd>
The native C++ implementation of this method defines a default argument
value. In the documentation generated for different libSBML language
bindings, you may or may not see corresponding arguments in the method
declarations. For example, in Java and C#, a default argument is handled by
declaring two separate methods, with one of them having the argument and
the other one lacking the argument. However, the libSBML documentation will
be <em>identical</em> for both methods. Consequently, if you are reading
this and do not see an argument even though one is described, please look
for descriptions of other variants of this method near where this one
appears in the documentation.
</dd></dl>
 
   */ public
 XMLTriple(String triplet) {
    this(libsbmlJNI.new_XMLTriple__SWIG_3(triplet), true);
  }

  
/**
   * Copy constructor; creates a copy of this {@link XMLTriple} set.
   * <p>
   * @param orig the {@link XMLTriple} object to copy.
   * <p>
   * @throws XMLConstructorException 
   * Thrown if the argument <code>orig</code> is <code>null.</code>
   */ public
 XMLTriple(XMLTriple orig) {
    this(libsbmlJNI.new_XMLTriple__SWIG_4(XMLTriple.getCPtr(orig), orig), true);
  }

  
/**
   * Creates and returns a deep copy of this {@link XMLTriple} set.
   * <p>
   * @return a (deep) copy of this {@link XMLTriple} set.
   */ public
 XMLTriple cloneObject() {
    long cPtr = libsbmlJNI.XMLTriple_cloneObject(swigCPtr, this);
    return (cPtr == 0) ? null : new XMLTriple(cPtr, true);
  }

  
/**
   * Returns the <em>name</em> portion of this {@link XMLTriple}.
   * <p>
   * @return a string, the name from this {@link XMLTriple}.
   */ public
 String getName() {
    return libsbmlJNI.XMLTriple_getName(swigCPtr, this);
  }

  
/**
   * Returns the <em>prefix</em> portion of this {@link XMLTriple}.
   * <p>
   * @return a string, the <em>prefix</em> portion of this {@link XMLTriple}.
   */ public
 String getPrefix() {
    return libsbmlJNI.XMLTriple_getPrefix(swigCPtr, this);
  }

  
/**
   * Returns the <em>URI</em> portion of this {@link XMLTriple}.
   * <p>
   * @return URI a string, the <em>prefix</em> portion of this {@link XMLTriple}.
   */ public
 String getURI() {
    return libsbmlJNI.XMLTriple_getURI(swigCPtr, this);
  }

  
/**
   * Returns the prefixed name from this {@link XMLTriple}.
   * <p>
   * @return a string, the prefixed name from this {@link XMLTriple}.
   */ public
 String getPrefixedName() {
    return libsbmlJNI.XMLTriple_getPrefixedName(swigCPtr, this);
  }

  
/**
   * Predicate returning <code>true</code> or <code>false</code> depending on whether 
   * this {@link XMLTriple} is empty.
   * <p>
   * @return <code>true</code> if this {@link XMLTriple} is empty, <code>false</code> otherwise.
   */ public
 boolean isEmpty() {
    return libsbmlJNI.XMLTriple_isEmpty(swigCPtr, this);
  }

}