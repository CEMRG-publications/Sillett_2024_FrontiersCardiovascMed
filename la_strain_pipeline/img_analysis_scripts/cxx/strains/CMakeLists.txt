
cmake_minimum_required(VERSION 3.3 FATAL_ERROR)

project(strains)

find_package(VTK COMPONENTS 
  vtkCommonColor
  vtkCommonCore
  vtkIOXML
  vtkInteractionStyle
  vtkRenderingContextOpenGL2
  vtkRenderingCore
  vtkRenderingFreeType
  vtkRenderingGL2PSOpenGL2
  vtkIOImage
  vtkFiltersSources
  vtkCommonDataModel
  vtkRenderingOpenGL2
  vtkInteractionImage
  vtkCommonSystem
  vtkIOGeometry
  vtkIOLegacy
  vtkIOPLY
  vtkFiltersGeneral QUIET)
if (NOT VTK_FOUND)
  message("Skipping strains: ${VTK_NOT_FOUND_MESSAGE}")
  return ()
endif()
message (STATUS "VTK_VERSION: ${VTK_VERSION}")
if (VTK_VERSION VERSION_LESS "8.90.0")
  # old system
  include(${VTK_USE_FILE})
  add_executable(strains MACOSX_BUNDLE strains.cxx )
  target_link_libraries(strains PRIVATE ${VTK_LIBRARIES})
else ()
  # include all components
  add_executable(strains MACOSX_BUNDLE strains.cxx )
  target_link_libraries(strains PRIVATE ${VTK_LIBRARIES})
  # vtk_module_autoinit is needed
  vtk_module_autoinit(
    TARGETS strains
    MODULES ${VTK_LIBRARIES}
    )
endif () 
