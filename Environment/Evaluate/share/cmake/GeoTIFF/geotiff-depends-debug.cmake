#----------------------------------------------------------------
# Generated CMake target import file for configuration "Debug".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "geotiff_library" for configuration "Debug"
set_property(TARGET geotiff_library APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_target_properties(geotiff_library PROPERTIES
  IMPORTED_LINK_INTERFACE_LIBRARIES_DEBUG "/home/cayang/anaconda3/envs/Evaluate/lib/libtiff.so;/home/cayang/anaconda3/envs/Evaluate/lib/libproj.so;/home/cayang/anaconda3/envs/Evaluate/lib/libz.so;/home/cayang/anaconda3/envs/Evaluate/lib/libjpeg.so"
  IMPORTED_LOCATION_DEBUG "${_IMPORT_PREFIX}/lib/libgeotiff.so.5.0.1"
  IMPORTED_SONAME_DEBUG "libgeotiff.so.5"
  )

list(APPEND _IMPORT_CHECK_TARGETS geotiff_library )
list(APPEND _IMPORT_CHECK_FILES_FOR_geotiff_library "${_IMPORT_PREFIX}/lib/libgeotiff.so.5.0.1" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
