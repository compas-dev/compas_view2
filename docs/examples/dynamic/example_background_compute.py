import time
from compas_view2.app import App
from compas.geometry import Point, Polyline, Bezier

curve = Bezier([[0, 0, 0], [3, 6, 0], [5, -3, 0], [10, 0, 0]])
viewer = App(viewmode="shaded", enable_sidebar=True, width=1600, height=900)

pointobj = viewer.add(Point(* curve.point(0)), pointsize=20, pointcolor=(1, 0, 0))
curveobj = viewer.add(Polyline(curve.locus()), linewidth=2)


@viewer.button(text="Compute")
def click():

    viewer.status(f"Starting computation in backgound...")

    # Function to be executed in the background thread.
    def compute(self, step, interval):

        i = 0
        while i < 1:
            time.sleep(interval)
            i += step
            # Direct interation with global variables like the `viewer` and `pointObj` from a background thread will cause errors.
            # Instead, `self.signals.progress.emit()` can be used to send out values to the main thread.
            # which can be received by the `on_progress` event listener provided below.
            self.signals.progress.emit(i)

        return i

    def on_progress(value):
        # This function will be triggered under main thread when `signals.progress.emit()` sends out value from background threads.
        viewer.status(f"waiting...t={value}")
        pointobj._data = curve.point(value)
        pointobj.update()
        viewer.view.update()

    def on_result(result):
        # This function will be triggered once the background thread finishes.
        viewer.status(f"Done, t={result}")
        viewer.info("Finished!")

    # `include_self=True` is provide in order to give "compute" function access to singal emit functions.
    viewer.threading(compute, args=[0.02, 0.2], on_progress=on_progress, on_result=on_result, include_self=True)


viewer.show()
