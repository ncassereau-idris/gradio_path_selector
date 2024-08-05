from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Sequence

import json
from pathlib import Path
from gradio.components.base import Component
from gradio.events import Events
from gradio.context import Context

if TYPE_CHECKING:
    from gradio.components import Timer


class FileExplorer(Component):

    """
    Creates a very simple textbox for user to enter string input or display string output.
    """

    EVENTS = [
        Events.change,
    ]

    def __init__(
        self,
        value: str | Callable | None = None,
        *,
        placeholder: str | None = None,
        label: str | None = None,
        every: Timer | float | None = None,
        show_label: bool | None = None,
        scale: int | None = None,
        min_width: int = 160,
        visible: bool = True,
        elem_id: str | None = None,
        elem_classes: list[str] | str | None = None,
        render: bool = True,
        key: int | str | None = None,
    ):
        """
        Parameters:
            value: default text to provide in textbox. If callable, the function will be called whenever the app loads to set the initial value of the component.
            placeholder: placeholder hint to provide behind textbox.
            label: component name in interface.
            every: Continously calls `value` to recalculate it if `value` is a function (has no effect otherwise). Can provide a Timer whose tick resets `value`, or a float that provides the regular interval for the reset Timer.
            show_label: if True, will display label.
            scale: relative size compared to adjacent Components. For example if Components A and B are in a Row, and A has scale=2, and B has scale=1, A will be twice as wide as B. Should be an integer. scale applies in Rows, and to top-level Components in Blocks where fill_height=True.
            min_width: minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.
            visible: If False, component will be hidden.
            elem_id: An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.
            elem_classes: An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.
            render: If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.
            key: if assigned, will be used to assume identity across a re-render. Components that have the same key across a re-render will have their value preserved.
        """
        self.placeholder = placeholder

        if value is None:
            value = self.init_value()
        super().__init__(
            label=label,
            every=every,
            show_label=show_label,
            scale=scale,
            min_width=min_width,
            visible=visible,
            elem_id=elem_id,
            elem_classes=elem_classes,
            value=value,
            render=render,
            key=key,
        )
        if Context.root_block is not None:
            self.subscribe()

    def subscribe(self):
        self.change(self.refresh_value, self, self)

    @staticmethod
    def get_listdir(path: Path) -> list[str]:
        # if path is None:
        #     path = Path.cwd()
        listdir = sorted(list(path.iterdir()))
        if len(listdir) > 0:
            return [p.name for p in listdir if p.is_dir()]
        else:
            return []

    @staticmethod
    def init_value() -> dict:
        return FileExplorer.get_value(Path.cwd())

    @staticmethod
    def get_value(path: Path) -> dict:
        return {
            "current_path": str(path),
            "available_directories": FileExplorer.get_listdir(path),
        }

    @staticmethod
    def refresh_value(D: dict):
        current_path = Path(D["current_path"])
        directory = D["selected_directory"]
        if directory == -1:
            path = current_path.parent
        else:
            path = current_path / directory
        return FileExplorer.get_value(path)

    def preprocess(self, payload: str | None) -> Path | None:
        """
        Parameters:
            payload: the text entered in the textarea.
        Returns:
            Passes text value as a {str} into the function.
        """
        if payload is None:
            return None
        else:
            return json.loads(payload)

    def postprocess(self, value: str | None) -> str | None:
        """
        Parameters:
            value: Expects a {str} returned from function and sets textarea value to it.
        Returns:
            The value to display in the textarea.
        """
        if value is None:
            return None
        else:
            value["status"] = "download"
            return json.dumps(value)

    def api_info(self) -> dict[str, Any]:
        return {"type": "string"}

    def example_payload(self) -> Any:
        return "Hello!!"

    def example_value(self) -> Any:
        return "Hello!!"
