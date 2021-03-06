/**
 * @file    SpatialExtensionTypes.h
 * @brief   Include all SBML types of spatial extension in a single header file.
 * @author  
 *
 * $Id: SpatialExtensionTypes.h 10152 2009-09-01 09:21:03Z sarahkeating $
 * $HeadURL: https://sbml.svn.sourceforge.net/svnroot/sbml/trunk/libsbml/src/sbml/SpatialExtensionTypes.h $
 *
 *<!---------------------------------------------------------------------------
 * This file is part of libSBML.  Please visit http://sbml.org for more
 * information about SBML, and the latest version of libSBML.
 *
 * Copyright 2005-2009 California Institute of Technology.
 * Copyright 2002-2005 California Institute of Technology and
 *                     Japan Science and Technology Corporation.
 * 
 * This library is free software; you can redistribute it and/or modify it
 * under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation.  A copy of the license agreement is provided
 * in the file named "LICENSE.txt" included with this software distribution
 * and also available online as http://sbml.org/software/libsbml/license.html
 *----------------------------------------------------------------------- -->*/

#ifndef SpatialExtensionTypes_h
#define SpatialExtensionTypes_h

#include <sbml/packages/spatial/common/spatialfwd.h>

#include <sbml/packages/spatial/extension/SpatialExtension.h>
#include <sbml/packages/spatial/extension/SpatialModelPlugin.h>
#include <sbml/packages/spatial/extension/SpatialParameterPlugin.h>
#include <sbml/packages/spatial/extension/SpatialSpeciesRxnPlugin.h>
#include <sbml/packages/spatial/extension/SpatialCompartmentPlugin.h>

#include <sbml/packages/spatial/sbml/Geometry.h>
#include <sbml/packages/spatial/sbml/CoordinateComponent.h>
#include <sbml/packages/spatial/sbml/Boundary.h>
#include <sbml/packages/spatial/sbml/DomainType.h>
#include <sbml/packages/spatial/sbml/CompartmentMapping.h>
#include <sbml/packages/spatial/sbml/Domain.h>
#include <sbml/packages/spatial/sbml/InteriorPoint.h>
#include <sbml/packages/spatial/sbml/AdjacentDomains.h>
#include <sbml/packages/spatial/sbml/AnalyticVolume.h>
#include <sbml/packages/spatial/sbml/AnalyticGeometry.h>
#include <sbml/packages/spatial/sbml/GeometryDefinition.h>
#include <sbml/packages/spatial/sbml/SampledFieldGeometry.h>
#include <sbml/packages/spatial/sbml/SampledVolume.h>
#include <sbml/packages/spatial/sbml/SampledField.h>
#include <sbml/packages/spatial/sbml/ImageData.h>
#include <sbml/packages/spatial/sbml/ParametricGeometry.h>
#include <sbml/packages/spatial/sbml/ParametricObject.h>
#include <sbml/packages/spatial/sbml/PolygonObject.h>
#include <sbml/packages/spatial/sbml/SpatialPoint.h>
#include <sbml/packages/spatial/sbml/CSGeometry.h>
#include <sbml/packages/spatial/sbml/CSGObject.h>
#include <sbml/packages/spatial/sbml/CSGNode.h>
#include <sbml/packages/spatial/sbml/CSGPrimitive.h>
#include <sbml/packages/spatial/sbml/CSGPseudoPrimitive.h>
#include <sbml/packages/spatial/sbml/CSGSetOperator.h>
#include <sbml/packages/spatial/sbml/CSGTransformation.h>
#include <sbml/packages/spatial/sbml/CSGTranslation.h>
#include <sbml/packages/spatial/sbml/CSGRotation.h>
#include <sbml/packages/spatial/sbml/CSGScale.h>
#include <sbml/packages/spatial/sbml/CSGHomogeneousTransformation.h>
#include <sbml/packages/spatial/sbml/TransformationComponents.h>
#include <sbml/packages/spatial/sbml/SpatialSymbolReference.h>
#include <sbml/packages/spatial/sbml/DiffusionCoefficient.h>
#include <sbml/packages/spatial/sbml/AdvectionCoefficient.h>
#include <sbml/packages/spatial/sbml/BoundaryCondition.h>

#endif  /* SpatialExtensionTypes_h */

