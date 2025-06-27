#include <vtkActor.h>
#include <vtkCamera.h>
#include <vtkNamedColors.h>
#include <vtkPolyDataMapper.h>
#include <vtkProperty.h>
#include <vtkRenderWindow.h>
#include <vtkRenderWindowInteractor.h>
#include <vtkRenderer.h>
#include <vtkSmartPointer.h>
#include <vtkXMLPolyDataReader.h>
#include <vtkPNGWriter.h>                 //new
#include <vtkWindowToImageFilter.h>       //new
#include <vtkVersion.h>                   //new
#include <vtkPolyData.h>                  //new
#include <vtkLight.h>                     //new
#include <vtkLightCollection.h>           //new
#include <vtksys/SystemTools.hxx>
#include "vtkPolyDataReader.h"
#include <vtkPolyDataNormals.h>
#include <vtkDataArray.h>
#include <vtkDoubleArray.h>
#include <vtkFloatArray.h>
#include <vtkCellData.h>
#include <vtkCellCenters.h>
#include <vtkDataSetMapper.h>
#include <vtkXMLUnstructuredGridReader.h>
#include <vtkDataSetSurfaceFilter.h>
#include <vtkUnstructuredGrid.h>
#include <vtkTriangle.h>
#include <vtkPoints.h>
#include <vtkMatrix3x3.h>
#include <vtkNew.h>
#include <vtkIdList.h>

using namespace std;

namespace
{
  vtkSmartPointer<vtkPolyData> ReadMesh( const char* filename );
}

void printarraydouble (double arg[], int length)
{
  for (int n=0; n<length; ++n)
    cout << arg[n] << ' ';
  cout << '\n';
}

void printarrayint (int arg[], int length)
{
  for (int n=0; n<length; ++n)
    cout << arg[n] << ' ';
  cout << '\n';
}

void Cross (double vec1[3], double vec2[3], double temp[3]);
double Norm (double vec1[3]);
double Dot(double vec1[3], double vec2[3]);

int main(int argc, char* argv[])
{
  // Parse command line arguments
  if (argc != 4)
  {
    std::cerr << "Usage: " << argv[0] << " Reference dcm0 mesh(.vtp/vtk/vtu); Tracked mesh (Number of cells should be equal); Fibre_name e.g. endo_1/endo_avg."
              << std::endl;
    return EXIT_FAILURE;
  }

  // Assign filename
  const char *file1 = 0;
  const char *file2 = 0;
  const char *file3 = 0;
  if (argc > 2)
  {
    file1 = argv[1];
    file2 = argv[2];
    file3 = argv[3];
  }

  // Load PolyData Meshes
  vtkSmartPointer<vtkPolyData> pdRef;
  vtkSmartPointer<vtkPolyData> pdTrk;
  pdRef = ReadMesh(file1);
  pdTrk = ReadMesh(file2);

  // Should have same number of cells
  cout << "Number of Cells RefMsh: " << pdRef->GetNumberOfCells() << endl;
  cout << "Number of Cells TrkMsh: " << pdTrk->GetNumberOfCells() << endl;

  // Generate cell normals
  vtkSmartPointer<vtkPolyDataNormals> normalGenerator = vtkSmartPointer<vtkPolyDataNormals>::New();
  normalGenerator->SetInputData(pdRef);
  normalGenerator->ComputePointNormalsOff();
  normalGenerator->ComputeCellNormalsOn();
  normalGenerator->Update();
  pdRef = normalGenerator->GetOutput();

  // Extract fibre direction
  // cout << "Using following fibre arch: " << file3 << endl;
  vtkSmartPointer<vtkDataArray> fibre = pdRef->GetCellData()->GetArray(file3);

  // Extract Normals
  vtkFloatArray* normalDataFloat = dynamic_cast<vtkFloatArray*>(pdRef->GetCellData()->GetArray("Normals"));

  // Calculate reference and current jacobian matrices for each cell
  for(vtkIdType cellID = 0; cellID < pdRef->GetNumberOfCells(); cellID++)
  {
    // cout << "Cell ID: " << cellID << endl;

    // Three nodes of the triangle

    // Ref configuration
    vtkSmartPointer<vtkCell> cellRef = pdRef->GetCell(cellID);
    vtkSmartPointer<vtkTriangle> triangleRef = dynamic_cast<vtkTriangle*>(cellRef.GetPointer());
    double pt1Ref[3], pt2Ref[3], pt3Ref[3];
    triangleRef->GetPoints()->GetPoint(0, pt1Ref);
    triangleRef->GetPoints()->GetPoint(1, pt2Ref);
    triangleRef->GetPoints()->GetPoint(2, pt3Ref);

    // Deformed configuration
    vtkSmartPointer<vtkCell> cellDef = pdTrk->GetCell(cellID);
    vtkSmartPointer<vtkTriangle> triangleDef = dynamic_cast<vtkTriangle*>(cellDef.GetPointer());
    double pt1Def[3], pt2Def[3], pt3Def[3];
    triangleDef->GetPoints()->GetPoint(0, pt1Def);
    triangleDef->GetPoints()->GetPoint(1, pt2Def);
    triangleDef->GetPoints()->GetPoint(2, pt3Def);

    // Coordinate system: Triangle vectors

    // Ref configuration
    double r1[3], r2[3], r3[3];

    r1[0] = pt2Ref[0] - pt1Ref[0];
    r1[1] = pt2Ref[1] - pt1Ref[1];
    r1[2] = pt2Ref[2] - pt1Ref[2];
    r2[0] = pt3Ref[0] - pt1Ref[0];
    r2[1] = pt3Ref[1] - pt1Ref[1];
    r2[2] = pt3Ref[2] - pt1Ref[2];

    Cross(r1, r2, r3);
    double normRef = Norm(r3);
    r3[0] = r3[0] / normRef;
    r3[1] = r3[1] / normRef;
    r3[2] = r3[2] / normRef;
    // cout << "Norm of r3: " << Norm(r3);

    // Def configuration
    double d1[3], d2[3], d3[3];

    d1[0] = pt2Def[0] - pt1Def[0];
    d1[1] = pt2Def[1] - pt1Def[1];
    d1[2] = pt2Def[2] - pt1Def[2];
    d2[0] = pt3Def[0] - pt1Def[0];
    d2[1] = pt3Def[1] - pt1Def[1];
    d2[2] = pt3Def[2] - pt1Def[2];

    Cross(d1, d2, d3);
    double normDef = Norm(d3);
    d3[0] = d3[0] / normDef;
    d3[1] = d3[1] / normDef;
    d3[2] = d3[2] / normDef; 
    // cout << "Norm of d3: " << Norm(d3);

    // Assemble Jref matrix
    // Reference configuation Jacobian
    vtkNew<vtkMatrix3x3> Jref;
    Jref->SetElement(0, 0, r1[0]);
    Jref->SetElement(0, 1, r2[0]);
    Jref->SetElement(0, 2, r3[0]);
    Jref->SetElement(1, 0, r1[1]);
    Jref->SetElement(1, 1, r2[1]);
    Jref->SetElement(1, 2, r3[1]);
    Jref->SetElement(2, 0, r1[2]);
    Jref->SetElement(2, 1, r2[2]);
    Jref->SetElement(2, 2, r3[2]);

    // cout << "Matrix Jref: " << endl;
    // cout << *Jref;

    // Assemble K/j matrix
    // Current configuration Jacobian
    vtkNew<vtkMatrix3x3> K;
    K->SetElement(0, 0, d1[0]);
    K->SetElement(0, 1, d2[0]);
    K->SetElement(0, 2, d3[0]);
    K->SetElement(1, 0, d1[1]);
    K->SetElement(1, 1, d2[1]);
    K->SetElement(1, 2, d3[1]);
    K->SetElement(2, 0, d1[2]);
    K->SetElement(2, 1, d2[2]);
    K->SetElement(2, 2, d3[2]);

    // cout << "Matrix K: " << endl;
    // cout << *K;

    // Calculate deofmration graident
    vtkNew<vtkMatrix3x3> F;
    vtkNew<vtkMatrix3x3> Jref_inv;
    vtkMatrix3x3::Invert(Jref, Jref_inv);

    // Checking matrix inversion
    // cout << "Jref matrix: " << endl;
    // cout << *Jref;
    // cout << "Jref_inv matrix: " << endl;
    // cout << *Jref_inv;

    vtkMatrix3x3::Multiply3x3(K, Jref_inv, F);

    // Check matrix multiplication?

    //Calculate Strain Tensors
    vtkNew<vtkMatrix3x3> ET;
    vtkNew<vtkMatrix3x3> EYE;

    //Green/Lagrange strain
    vtkNew<vtkMatrix3x3> FT;
    vtkNew<vtkMatrix3x3> FT_F;
    vtkMatrix3x3::Transpose(F, FT);
    vtkMatrix3x3::Multiply3x3(FT, F, FT_F);

    // Checking FT_F matrix
    // cout << "FT_F matrix: " << endl;
    // cout << *FT_F;

    // FT*F - Identity matrix
    FT_F->SetElement(0, 0, FT_F->GetElement(0, 0) - 1.0);
    FT_F->SetElement(1, 1, FT_F->GetElement(1, 1) - 1.0);
    FT_F->SetElement(2, 2, FT_F->GetElement(2, 2) - 1.0);

    // Checking Identity matrix subtraction
    // cout << "FT_F - identity: " << endl;
    // cout << *FT_F;

    // ET = 0.5*(FT_F - Identity)
    ET->SetElement(0, 0, FT_F->GetElement(0, 0)*0.5);
    ET->SetElement(0, 1, FT_F->GetElement(0, 1)*0.5);
    ET->SetElement(0, 2, FT_F->GetElement(0, 2)*0.5);
    ET->SetElement(1, 0, FT_F->GetElement(1, 0)*0.5);
    ET->SetElement(1, 1, FT_F->GetElement(1, 1)*0.5);
    ET->SetElement(1, 2, FT_F->GetElement(1, 2)*0.5);
    ET->SetElement(2, 0, FT_F->GetElement(2, 0)*0.5);
    ET->SetElement(2, 1, FT_F->GetElement(2, 1)*0.5);
    ET->SetElement(2, 2, FT_F->GetElement(2, 2)*0.5);

    // Checking Half multiplication
    // cout << "0.5*(FT_F - identity): " << endl;
    // cout << *ET;

    // Rotate into fibre basis

    // Extract fibre direction from each cell.
    // Construct fibre basis from this for each cell.
    // Find basis transformation matrix
    // Use this to rotate ET, and read off diagonal elements

    // Extract fibre basis
    double cell_fib_1[3];
    double cell_fib_2[3];
    double cell_fib_3[3];

    // cell_fib_1[0] = 0.0;
    // cell_fib_1[1] = 0.0;
    // cell_fib_1[2] = 1.0;
    // double norm_cell_fib_1 = Norm(cell_fib_1);
    // cell_fib_1[0] = cell_fib_1[0] / norm_cell_fib_1;
    // cell_fib_1[1] = cell_fib_1[1] / norm_cell_fib_1;
    // cell_fib_1[2] = cell_fib_1[2] / norm_cell_fib_1;

    // Assign fibre 1
    fibre->GetTuple(cellID, cell_fib_1);

    // Get Normal direction for fibre 3
    double normal[3];
    normalDataFloat->GetTuple(cellID, normal);
    double normal_norm = Norm(normal);

    // cout << "normal_norm: " << normal_norm << endl;

    cell_fib_3[0] = normal[0] / normal_norm;
    cell_fib_3[1] = normal[1] / normal_norm;
    cell_fib_3[2] = normal[2] / normal_norm;

    // Get fibre 2 from cross product
    Cross(cell_fib_3, cell_fib_1, cell_fib_2);

    // // Checking dot product is 0
    // double dot_check;
    // dot_check = Dot(cell_fib_1, cell_fib_2);
    // cout << "dot: " << dot_check << endl;

    // Cross(cell_fib_1, cell_fib_2, cell_fib_3);
    // double norm_cell_fib_3 = Norm(cell_fib_3);
    // cell_fib_3[0] = cell_fib_3[0] / norm_cell_fib_3;
    // cell_fib_3[1] = cell_fib_3[1] / norm_cell_fib_3;
    // cell_fib_3[2] = cell_fib_3[2] / norm_cell_fib_3; 

    // cout << "cell fib 1: " << cell_fib_1[0] << " " << cell_fib_1[1] << " " << cell_fib_1[2] << endl; 
    // cout << "cell fib 2: " << cell_fib_2[0] << " " << cell_fib_2[1] << " " << cell_fib_2[2] << endl;
    // cout << "cell fib 3: " << cell_fib_3[0] << " " << cell_fib_3[1] << " " << cell_fib_3[2] << endl;

    // Basis Transformation
    vtkNew<vtkMatrix3x3> Q_fib;
    vtkNew<vtkMatrix3x3> Q_fibT;
    Q_fib->SetElement(0, 0, cell_fib_1[0]); // first row 3 cols
    Q_fib->SetElement(0, 1, cell_fib_2[0]);
    Q_fib->SetElement(0, 2, cell_fib_3[0]);
    Q_fib->SetElement(1, 0, cell_fib_1[1]); // second row 3 cols
    Q_fib->SetElement(1, 1, cell_fib_2[1]);
    Q_fib->SetElement(1, 2, cell_fib_3[1]);
    Q_fib->SetElement(2, 0, cell_fib_1[2]); // third row 3 cols
    Q_fib->SetElement(2, 1, cell_fib_2[2]);
    Q_fib->SetElement(2, 2, cell_fib_3[2]);
    vtkMatrix3x3::Transpose(Q_fib, Q_fibT);

    // E = Q*ET*Q_T
    vtkNew<vtkMatrix3x3> E;
    vtkNew<vtkMatrix3x3> Q_ET;
    vtkMatrix3x3::Multiply3x3(Q_fib, ET, Q_ET);
    vtkMatrix3x3::Multiply3x3(Q_ET, Q_fibT, E);

    // Read off diagonal strains for fibre strains
    // cout << "Final E matrix following rotation into fibre basis." << endl;
    // cout << *E << endl;    // print E matrix

    // Dot product with normals to get strain components
    double E_fib1;
    double E_fib2;
    double E_fib3;

    double ET_fib1;
    double ET_fib2;
    double ET_fib3;

    double E_cell_fib_1[3];
    double E_cell_fib_2[3];
    double E_cell_fib_3[3];

    double ET_cell_fib_1[3];
    double ET_cell_fib_2[3];
    double ET_cell_fib_3[3];

    // Rotated E
    E->MultiplyPoint(cell_fib_1, E_cell_fib_1);
    E->MultiplyPoint(cell_fib_2, E_cell_fib_2);
    E->MultiplyPoint(cell_fib_3, E_cell_fib_3);
    
    E_fib1 = Dot(cell_fib_1, E_cell_fib_1);
    E_fib2 = Dot(cell_fib_2, E_cell_fib_2);
    E_fib3 = Dot(cell_fib_3, E_cell_fib_3);


    // UnRotated E
    ET->MultiplyPoint(cell_fib_1, ET_cell_fib_1);
    ET->MultiplyPoint(cell_fib_2, ET_cell_fib_2);
    ET->MultiplyPoint(cell_fib_3, ET_cell_fib_3);

    ET_fib1 = Dot(cell_fib_1, ET_cell_fib_1);
    ET_fib2 = Dot(cell_fib_2, ET_cell_fib_2);
    ET_fib3 = Dot(cell_fib_3, ET_cell_fib_3);

    // cout << "E matrix: " << *E << endl;

    // cout << "E diagonals: " << E->GetElement(0,0) << " " << E->GetElement(1,1) << " " << E->GetElement(2,2) << endl;
    // cout << "e_tilda diagonals: " << e_tilda->GetElement(0,0) << " " << e_tilda->GetElement(1,1) << " " << e_tilda->GetElement(2,2) << endl;
    // cout << "E fib diagonals: " << E_fib1 << " " << E_fib2 << " " << E_fib3 << endl;
    cout << ET_fib1 << " " << ET_fib2 << " " << ET_fib3 << endl;

    // cout fibres
    // cout << "f1: " << cell_fib_1[0] << " " << cell_fib_1[1] << " " << cell_fib_1[2] << endl;
    // cout << "f2: " << cell_fib_2[0] << " " << cell_fib_2[1] << " " << cell_fib_2[2] << endl;
    // cout << "f3: " << cell_fib_3[0] << " " << cell_fib_3[1] << " " << cell_fib_3[2] << endl;
  }

  return EXIT_SUCCESS;
}

namespace
{
  vtkSmartPointer<vtkPolyData> ReadMesh( const char* filename )
  {
    vtkSmartPointer<vtkPolyData> polydata;

    // Get file extension
    std::string extension = vtksys::SystemTools::GetFilenameLastExtension(std::string(filename));

    // Drop the case of the extension
    std::transform(extension.begin(), extension.end(), extension.begin(), ::tolower);

    if (extension == ".vtp")
    {
      vtkSmartPointer<vtkXMLPolyDataReader> PolyDatareader = vtkSmartPointer<vtkXMLPolyDataReader>::New();
      PolyDatareader->SetFileName(filename);
      PolyDatareader->Update();
      polydata = PolyDatareader->GetOutput();
    }

    if (extension == ".vtu")
    {
      auto UnstructGridreader = vtkSmartPointer<vtkXMLUnstructuredGridReader>::New();
      UnstructGridreader->SetFileName (filename);
      UnstructGridreader->Update();

      vtkSmartPointer<vtkUnstructuredGrid> pdTrackedUnstructGrid;
      pdTrackedUnstructGrid = UnstructGridreader->GetOutput();

      vtkSmartPointer<vtkDataSetSurfaceFilter> surfaceFilter = vtkSmartPointer<vtkDataSetSurfaceFilter>::New();
      surfaceFilter->SetInputData(pdTrackedUnstructGrid);
      surfaceFilter->Update();

      polydata = surfaceFilter->GetOutput();
    }

    else if (extension == ".vtk")
    {
      auto PolyDatareader = vtkSmartPointer<vtkPolyDataReader>::New();
      PolyDatareader->SetFileName (filename);
      PolyDatareader->Update();
      polydata = PolyDatareader->GetOutput();
    }

    return polydata;
  }
}

void Cross(double vec1[3], double vec2[3], double ans[3]) {

    ans[0] = vec1[1] * vec2[2] - vec1[2] * vec2[1];
    ans[1] = vec1[2] * vec2[0] - vec1[0] * vec2[2];
    ans[2] = vec1[0] * vec2[1] - vec1[1] * vec2[0];
}

double Norm(double vec1[3]) {

    double norm;
    norm = sqrt(pow(double(vec1[0]), 2.0) +
        pow(double(vec1[1]), 2.0) +
        pow(double(vec1[2]), 2.0));
    return norm;
}

double Dot(double vec1[3], double vec2[3]) {
  
  double dot_product;
  dot_product = vec1[0] * vec2[0] + vec1[1] * vec2[1] + vec1[2] * vec2[2];

  return dot_product;
}