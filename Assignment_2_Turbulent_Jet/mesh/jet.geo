//----------------------------------------------------------------------
// Adhith Krishna - GSoC 2026 Submission Assignment 2
// Axisymmetric Turbulent Jet - Gmsh Geometry and Meshing Script
// 
// Made to match:
// 1) Fukushima et al. (2001) PIV/LIF experiment and thereby also
// 2) Boersma et al. (1998) Inflow conditions of round jet and
// 3) Hussein et al. (1994) Velocity measurements in axisymmetric
// turbulent jet
// 
// By convention,
// x = axial, y = radial and y = 0 is the axis
//
// Non-Dimensional units,
// D=2 (radius R = 1), //2 to avoid R=0.5
//
// Fluid Domain:
// 300D axial (i.e. x=0 to 600), 55D radial (y=0 to 100)
//
// Rough Geometry Sketch:
//
//  P3 (0,110) ------Top Wall------- P4 (600,110)
//     |                                    |
//     |                                    |
//     |                                    |
//     |                                    |
//  P2 (0,1) (Inlet)                        | (Outlet)
//     |                                    |
//     |                                    |
//     |                                    |
//     |                                    |
//  P1 (0,0) ----------Axis----------- P5 (600,0)
//
//  Loop traversal: P1->P2->P3->P4->P5->P1 (CCW)
//----------------------------------------------------------------------
//
//----------------------------------------------------------------------
// 1. Mesh Sizing Parameters
//----------------------------------------------------------------------
//
// Experimented with values to obtain an overall mesh size between 300k
// to 400k to compute within a reasonable time period.
//
lc_far = 5.0;
lc_wall = 1.0;
lc_axis = 0.5;
lc_lip = 0.3;
lc_inlet = 0.4;
//
//----------------------------------------------------------------------
// 2. Coordinates, Lines, Loops and Surfaces
//----------------------------------------------------------------------
//
Point(1) = {0, 0, 0, lc_inlet}; //nozzle exit
Point(2) = {0, 1, 0, lc_lip}; // nozzle lip
Point(3) = {0, 110, 0, lc_wall}; // Top Left Corner
Point(4) = {90, 110, 0, lc_wall}; // Top Right Corner
Point(5) = {90, 0, 0, lc_axis}; // Outlet point on axis
Line(1) = {1, 2};   // jet_inlet
Line(2) = {2, 3};   // nozzle_plate
Line(3) = {3, 4};   // top_wall
Line(4) = {4, 5};   // outlet
Line(5) = {5, 1};   // axis
Curve Loop(1) = {1, 2, 3, 4, 5};
Plane Surface(1) = {1};
//
//----------------------------------------------------------------------
// 3. Mesh Refinement
//----------------------------------------------------------------------
//
// Grades the mesh smoothly from the nozzle lip to outlet
//
// - 1 and 2 refines the mesh to radiate outward from a single point 
// at the lip of the nozzle
// - 3 and 4 refines the mesh outward from the inlet segment 
// - 5 and 6 refines the mesh radially with higher density at the
// axis
// - 7 and 8 refines the mesh outward from the nozzle plate 
// - 9 and 10 refines the mesh at the top plane
// - 11 ensures than the most refined segment is picked at all 
// points
//
Field[1] = Distance; 
Field[1].PointsList = {2};
Field[2] = Threshold; 
//
Field[2].InField = 1;
Field[2].SizeMin = lc_lip;
Field[2].SizeMax = lc_far;
Field[2].DistMin = 1.5; 
Field[2].DistMax = 10.0;
//
Field[3] = Distance;
Field[3].CurvesList = {1};
Field[3].NNodesByEdge   = 100;
//
Field[4] = Threshold;
Field[4].InField  = 3;
Field[4].SizeMin  = lc_inlet;
Field[4].SizeMax  = lc_far;
Field[4].DistMin  = 1.0;
Field[4].DistMax  = 10.0;
//
Field[5] = Distance;
Field[5].CurvesList = {5};
Field[5].NNodesByEdge   = 90;
//
Field[6] = Threshold;
Field[6].InField  = 5;
Field[6].SizeMin  = lc_axis;
Field[6].SizeMax  = lc_far;
Field[6].DistMin  = 0.5;
Field[6].DistMax  = 5.0;
//
Field[7] = Distance;
Field[7].CurvesList = {2};
Field[7].NNodesByEdge   = 300;
//
Field[8] = Threshold;
Field[8].InField  = 7;
Field[8].SizeMin  = lc_wall;
Field[8].SizeMax  = lc_far;
Field[8].DistMin  = 0.5;
Field[8].DistMax  = 5.0;
//
Field[9] = Distance;
Field[9].CurvesList = {3};
Field[9].NNodesByEdge   = 90;
//
Field[10] = Threshold;
Field[10].InField  = 9;
Field[10].SizeMin  = lc_wall;
Field[10].SizeMax  = lc_far;
Field[10].DistMin  = 0.5;
Field[10].DistMax  = 5.0;
//
Field[11] = Min;
Field[11].FieldsList = {2, 4, 6, 8, 10};
//
Background Field = 11;
//
//----------------------------------------------------------------------
// 4. Physical Groups
//----------------------------------------------------------------------
Physical Curve("jet_inlet")    = {1};
Physical Curve("nozzle_plate") = {2};
Physical Curve("top_wall")     = {3};
Physical Curve("outlet")       = {4};
Physical Curve("axis")         = {5};
//
Physical Surface("fluid")      = {1};
//
//---------------------------------------------------------------------
// 5. Meshing algorithm settings
//---------------------------------------------------------------------
//
// The Frontal-Delaunay algorithm was chosen over other options as it 
// helps with maintaining the aspect ratio within triangles of the
// mesh, especially at wall boundaries.
//
Mesh.Algorithm        = 6;
Mesh.RecombineAll     = 0;
Mesh.CharacteristicLengthExtendFromBoundary = 1;
Mesh.CharacteristicLengthFromPoints         = 1;
Mesh.CharacteristicLengthFromCurvature      = 0;
Mesh.Optimize         = 1;
Mesh.OptimizeNetgen   = 1;
//
//---------------------------------------------------------------------
// fin.
//---------------------------------------------------------------------
