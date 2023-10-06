import os

files = os.listdir("examples")
img_files = os.listdir("_images")
for file in files:
    file_name = file.replace(".py", "")  # Like "example_csg_flow.py"
    title = file_name.replace("example_", "").replace("_", " ").title()
    for i, img_file in enumerate(img_files):
        if img_file == file_name + ".jpg":
            img_name = file_name + ".jpg"  # Like "example_csg_flow.jpg"
            break
        elif  img_file == file_name + ".gif":
            img_name = file_name + ".gif"  # Like "example_csg_flow.gif"
            break
        elif i == len(img_files) - 1:
            print ("No image found for " + file_name)
            exit(1)


    f = open(os.path.join("examples/"+file_name+".rst"),"x")
    f.write("*******************************************************************************")
    f.write('\n')
    f.write(title)
    f.write('\n')
    f.write("*******************************************************************************")
    f.write('\n')
    f.write('\n')

    f.write('.. figure:: /_images/'+img_name)
    f.write('\n')

    f.write('    :figclass: figure')
    f.write('\n')

    f.write("    :class: figure-img img-fluid")
    f.write('\n')

    f.write('\n')
    f.write(".. literalinclude:: "+ file_name + ".py")
    f.write('\n')
    f.write("    :language: python")
    f.write('\n')
