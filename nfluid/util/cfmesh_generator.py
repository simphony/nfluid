import sys
import os
import ntpath
import shutil
import nfluid.util.stl as stl


def make_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def generate_cfmesh_project(file_path, template_name=None):

    path = os.path.dirname(stl.__file__)
    if template_name is None:
        template_const = 'foam_files\\cfmesh_templates\\cfmeshTemplate.txt'
        template_name = os.path.join(path, template_const)

    base_name = ntpath.basename(file_path)
    case_name, file_ext = os.path.splitext(base_name)

    if os.path.exists('CFMESH_PROJECT'):
        shutil.rmtree('CFMESH_PROJECT')

    make_dir('CFMESH_PROJECT\\constant\\triSurface')
    make_dir('CFMESH_PROJECT\\system')

    shutil.copy2(file_path, 'CFMESH_PROJECT\\constant\\triSurface\\' +
                 case_name + '.stl')

    shutil.copy2(path + '\\foam_files\\common_files\\controlDict',
                     'CFMESH_PROJECT\\system\\')
    shutil.copy2(path + '\\foam_files\\common_files\\fvSchemes',
                     'CFMESH_PROJECT\\system\\')
    shutil.copy2(path + '\\foam_files\\common_files\\fvSolution',
                     'CFMESH_PROJECT\\system\\')


    search_words = [
        '$$$STL_FILE_NAME$$$'
        ]

    replacement = len(search_words) * [None]

    replacement[0] = '\\constant\\triSurface\\' + \
                     case_name + file_ext

    ft = open(template_name, 'r')
    fo = open('CFMESH_PROJECT\\system\\meshDict', 'w')

    for n_str in ft:
        for i in xrange(len(search_words)):
            n_str = n_str.replace(search_words[i], replacement[i])
        fo.write(n_str)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print 'cfMesh (tetMesh) Project Generator'
        print 'Usage:'
        print '\tpython cfmesh_generator.py'
        print '\t\t<STL_file_name>'
        print '\t\t[template_file_path="foam_files/cfmesh_templates/' + \
              'cfmeshTemplate.txt"]'
        exit(0)

    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = 'my_file.stl'

    if len(sys.argv) > 2:
        template_name = sys.argv[2]
    else:
        template_name = 'foam_files/cfmesh_templates/cfmeshTemplate.txt'


    generate_cfmesh_project(file_path, template_name)
