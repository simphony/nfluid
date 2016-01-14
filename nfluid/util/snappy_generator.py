import sys
import os
import ntpath
import shutil
import nfluid.util.stl as stl


def make_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def CreateBlockMeshDict(f, minv, maxv, nx, ny, nz):

    f.write('FoamFile\n')
    f.write('{\n')
    f.write('    version     2.0;\n')
    f.write('    format      ascii;\n')
    f.write('    class       dictionary;\n')
    f.write('    object      blockMeshDict;\n')
    f.write('}\n')
    f.write('// * * * * * * * * * * * * * * * * * * * * //\n')
    f.write('\n')

    f.write('convertToMeters 1;\n')
    f.write('\n')

    f.write('  vertices\n')
    f.write('  (\n')

    f.write("      (" + str(minv[0]) + ' ' +
            str(minv[1]) + ' ' + str(minv[2]) + ')\n')
    f.write("      (" + str(maxv[0]) + ' ' +
            str(minv[1]) + ' ' + str(minv[2]) + ')\n')
    f.write("      (" + str(maxv[0]) + ' ' +
            str(maxv[1]) + ' ' + str(minv[2]) + ')\n')
    f.write("      (" + str(minv[0]) + ' ' +
            str(maxv[1]) + ' ' + str(minv[2]) + ')\n')

    f.write("      (" + str(minv[0]) + ' ' +
            str(minv[1]) + ' ' + str(maxv[2]) + ')\n')
    f.write("      (" + str(maxv[0]) + ' ' +
            str(minv[1]) + ' ' + str(maxv[2]) + ')\n')
    f.write("      (" + str(maxv[0]) + ' ' +
            str(maxv[1]) + ' ' + str(maxv[2]) + ')\n')
    f.write("      (" + str(minv[0]) + ' ' +
            str(maxv[1]) + ' ' + str(maxv[2]) + ')\n')

    f.write('  );\n')

    f.write('\n')
    f.write('  blocks\n')
    f.write('  (\n')
    f.write('    hex (0 1 2 3 4 5 6 7) (' + str(nx) + ' ' + str(ny) + ' ' +
            str(nz) + ') simpleGrading (1 1 1)\n')
    f.write('  );\n')

    f.write('\n')
    f.write('  edges\n')
    f.write('  (\n')
    f.write('  );\n')

    f.write('\n')
    f.write('  boundary\n')
    f.write('  (\n')
    f.write('  );\n')


def generate_snappy_project(file_path, template_name=None,
                            ncells_x=20, ncells_y=20, ncells_z=20):

    if template_name is None:
        path = os.path.dirname(stl.__file__)
        template_name = os.path.join(path,
                                     'snappy_templates\\SnappyTemplate.txt')

    base_name = ntpath.basename(file_path)
    case_name, file_ext = os.path.splitext(base_name)

    if os.path.exists('FOAM_PROJECT'):
        shutil.rmtree('FOAM_PROJECT')

    make_dir('FOAM_PROJECT\\constant\\polyMesh')
    make_dir('FOAM_PROJECT\\constant\\triSurface')
    make_dir('FOAM_PROJECT\\system')

    shutil.copy2(file_path, 'FOAM_PROJECT\\constant\\triSurface\\' +
                 case_name + '.stl')

    stlinfo = stl.STL_Info(file_path)
    minv = (stlinfo.minx, stlinfo.miny, stlinfo.minz)
    maxv = (stlinfo.maxx, stlinfo.maxy, stlinfo.maxz)

    fb = open('FOAM_PROJECT\\constant\\polyMesh\\blockMeshDict', 'w')
    CreateBlockMeshDict(fb, minv, maxv, ncells_x, ncells_y, ncells_z)

    search_words = [
        '$$$STL_FILE_NAME$$$',
        '$$$TASK_NAME$$$',
        '$$$REFINEMENT_BOX_MIN$$$',
        '$$$REFINEMENT_BOX_MAX$$$']

    replacement = len(search_words) * [None]

    replacement[0] = case_name + file_ext
    replacement[1] = case_name
    replacement[2] = str(minv[0]) + ' ' + str(minv[1]) + ' ' + str(minv[2])
    replacement[3] = str(maxv[0]) + ' ' + str(maxv[1]) + ' ' + str(maxv[2])

    # ft = open('TEMPLATES/' + template_name, 'r')
    ft = open(template_name, 'r')
    fo = open('FOAM_PROJECT\\system\\snappyHexMeshDict', 'w')

    for n_str in ft:
        for i in xrange(len(search_words)):
            n_str = n_str.replace(search_words[i], replacement[i])
        fo.write(n_str)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print 'Snappy Hex Mesh Project Generator'
        print 'Usage:'
        print '\tpython snappy_generator.py'
        print '\t\t<STL_file_name>'
        print '\t\t[template_file_path="SnappyTemplate.txt"]'
        print '\t\t[ncells_x=20] [ncells_y=20] [ncells_z=20]'
        exit(0)

    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = 'my_file.stl'

    if len(sys.argv) > 2:
        template_name = sys.argv[2]
    else:
        template_name = 'SnappyTemplate.txt'

    if len(sys.argv) > 3:
        ncells_x = int(sys.argv[3])
    else:
        ncells_x = 20

    if len(sys.argv) > 4:
        ncells_y = int(sys.argv[4])
    else:
        ncells_y = 20

    if len(sys.argv) > 5:
        ncells_z = int(sys.argv[5])
    else:
        ncells_z = 20

    generate_snappy_project(file_path, template_name,
                            ncells_x, ncells_y, ncells_z)
