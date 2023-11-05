import compas_view2
import matplotlib.image as mpimg


viewer = compas_view2.app.App(width=1920, height=1080)  # Create a compas_view2 viewer

figure = viewer.plot(min_height=450)  # Create a figure within the viewer to display the image

img_src = compas_view2.get("/imag_1920_400_placehold.png")  # Load the image
image_data = mpimg.imread(img_src)

figure.figimage(image_data, cmap="gray", interpolation="nearest")  # Display the image on the figure

viewer.show()
