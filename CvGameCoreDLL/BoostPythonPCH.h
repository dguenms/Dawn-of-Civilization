#pragma once

#ifndef BOOST_PYTHON_PCH_H
#define BOOST_PYTHON_PCH_H

// advc: Moved out of CvGameCoreDLL.h for tidiness

/*	<advc.make> (This prevents many error markers in the VS code editor, but not all.)
	For VS users who don't bother to set up the Boost paths. */
#ifdef _CODE_EDITOR
namespace boost
{
	namespace python
	{
		class tuple;
		template<typename x, typename y> class class_;
		template<typename x> class return_value_policy;
		class reference_existing_object;
	}
	class noncopyable {}; // advc.003e
	// <advc> Might want to use these at some point
	template<typename T>
	struct shared_ptr { T t; shared_ptr(T*) {}; T& operator*() { return t; } };
	template<typename T>
	struct scoped_ptr { T t; scoped_ptr(T*) {}; T& operator*() { return t; } };
	// </advc>
}
#define BOOST_STATIC_ASSERT(expr)
class PyObject;
#else // </advc.make>
# include <boost/python/list.hpp>
# include <boost/python/tuple.hpp>
# include <boost/python/class.hpp>
# include <boost/python/manage_new_object.hpp>
# include <boost/python/return_value_policy.hpp>
# include <boost/python/object.hpp>
# include <boost/python/def.hpp>
# include <boost/python/enum.hpp> // advc.make: Moved from CyEnumsInterface.cpp
# include <boost/python/overloads.hpp> // advc.make: Moved from CyRandomInterface.cpp

namespace python = boost::python;
#endif // advc.make

#endif
