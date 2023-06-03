import datetime as dt
import uuid

from .bootstrap_HTML import *
from js import document, FileReader, btoa, Uint8Array   # type: ignore
from pyodide.ffi import create_proxy  # type: ignore
import io
import base64


class InputLabel(HTML.Label, BootstrapContainer):
    _default_class_name: str = "form-label"


class InputLabelCheckbox(InputLabel):
    _default_class_name: str = "form-check-label"


class InputHelp(BootstrapContainer):
    _default_class_name: str = "form-text"


class InputFormControl(HTML.Input, BootstrapContainer):
    _default_class_name: str = "form-control"


class InputFormControlColor(InputFormControl):
    _default_class_name: str = "form-control form-control-color"


class InputFormControlNumber(InputFormControl):
    _default_class_name: str = "form-control"

    @property
    def min(self):
        return self.element.getAttribute("min")

    @min.setter
    def min(self, value):
        self.element.setAttribute("min", str(value))

    @property
    def max(self):
        return self.element.getAttribute("max")

    @max.setter
    def max(self, value):
        self.element.setAttribute("max", str(value))


class InputFormControlRange(InputFormControl):
    _default_class_name: str = "form-range"


class InputFormControlSelect(InputFormControl):
    _default_class_name: str = "form-select"
    _tag_type: str = "select"


class InputFormControlCheckbox(InputFormControl):
    _default_class_name: str = "form-check-input"


class InputElement(BootstrapContainer):

    _default_input_type = "text"
    _default_input_class = InputFormControl
    _default_label_class = InputLabel

    def __init__(self,
                 label_text: str = None,
                 help_text: str = None,
                 floating_label: bool = False,
                 placeholder: str = None,
                 input_type=None,
                 id=None,
                 parent=None):
        super().__init__(parent=parent, id=id)

        if floating_label and placeholder is None:
            placeholder = " "  # create a dummy placeholder

        self._input = self.__class__._default_input_class(
            parent=None,
            id=self.id+"_input",
            type=input_type if input_type is not None else self._default_input_type,
            placeholder=placeholder
        )

        self._label = self.__class__._default_label_class(
            parent=None, id=self.id+"_label", inner_html=label_text)

        # if floating_label is True, add the input first, then the label

        if floating_label:
            self.append_child(self._input)
            self.append_child(self._label)

        else:
            self.append_child(self._label)
            self.append_child(self._input)

        self._help_text = None
        if help_text is not None:
            self._help_text = InputHelp(
                parent=self, id=self.id+"_help_text", inner_html=help_text)

        self.floating_label = floating_label

    @property
    def is_small(self) -> bool:
        return self._input.has_class("form-control-sm")

    @is_small.setter
    def is_small(self, value: bool):
        self._input.set_class_name("form-control-sm", value)

    @property
    def is_large(self) -> bool:
        return self._input.has_class("form-control-lg")

    @is_large.setter
    def is_large(self, value: bool):
        self._input.set_class_name("form-control-lg", value)

    @property
    def readonly(self) -> bool:
        return self._input.has_attribute("readonly")

    @readonly.setter
    def readonly(self, value: bool):
        self._input.set_attribute("readonly", value, is_boolean_attribute=True)

    @property
    def value(self):
        return self._input.value

    @value.setter
    def value(self, value):
        self._input.value = value

    @property
    def onchange(self):
        return self._input.onchange

    @onchange.setter
    def onchange(self, value):
        self._input.onchange = value

    @property
    def floating_label(self) -> bool:
        return self.has_class("form-floating")

    @floating_label.setter
    def floating_label(self, value: bool):
        self.set_class("form-floating", value)


class InputEmail(InputElement):
    _default_input_type = "email"


class InputPassword(InputElement):
    _default_input_type = "password"


class InputText(InputElement):
    _default_input_type = "text"


class InputFloat(InputElement):
    _default_input_type = "number"
    _default_number_class = float

    def __init__(self,
                 label_text: str = None,
                 help_text: str = None,
                 floating_label: bool = False,
                 placeholder: str = None,
                 min: _default_number_class = None,
                 max: _default_number_class = None,
                 step: _default_number_class = None,
                 input_type=None,
                 id=None,
                 parent=None):
        super().__init__(label_text=label_text,
                         help_text=help_text,
                         floating_label=floating_label,
                         placeholder=placeholder,
                         input_type=input_type,
                         id=id,
                         parent=parent)

        if min is not None:
            self.min = min

        if max is not None:
            self.max = max

        if step is not None:
            self.step = step

    @property
    def value(self) -> _default_number_class:
        val = self._input.value
        if val == "":
            return None
        return self.__class__._default_number_class(self._input.value)

    @value.setter
    def value(self, value: _default_number_class):
        self._input.value = str(value) if value is not None else ""

    @property
    def min(self) -> _default_number_class:
        return self.__class__._default_number_class(self._input.get_attribute("min"))

    @min.setter
    def min(self, value: _default_number_class):
        self._input.set_attribute("min", str(value))

    @property
    def max(self) -> _default_number_class:
        return self.__class__._default_number_class(self._input.get_attribute("max"))

    @max.setter
    def max(self, value: _default_number_class):
        self._input.set_attribute("max", str(value))

    @property
    def step(self) -> _default_number_class:
        return self.__class__._default_number_class(self._input.get_attribute("step"))

    @step.setter
    def step(self, value: _default_number_class):
        self._input.set_attribute("step", str(value))


class InputRangeFloat(InputFloat):
    _default_input_type = "range"
    _default_input_class = InputFormControlRange


class InputInt(InputFloat):

    _default_number_class = int


class InputRangeInt(InputInt):
    _default_input_type = "range"
    _default_input_class = InputFormControlRange


class InputDate(InputElement):
    _default_input_type = "date"

    @property
    def value(self) -> dt.datetime:
        if self._input.value == "":
            return None
        return dt.datetime.strptime(self._input.value, "%Y-%m-%d").date()

    @value.setter
    def value(self, value: Union[dt.datetime, dt.date, str, None]):
        if isinstance(value, str):
            self._input.value = value
        self._input.value = value.strftime(
            "%Y-%m-%d") if value is not None else ""


class InputTime(InputElement):
    _default_input_type = "time"

    @property
    def value(self) -> dt.datetime:
        if self._input.value == "":
            return None
        return dt.datetime.strptime(self._input.value, "%H:%M").time()

    @value.setter
    def value(self, value: Union[dt.datetime, dt.time, str, None]):
        if isinstance(value, str):
            self._input.value = value
        self._input.value = value.strftime(
            "%H:%M") if value is not None else ""


class InputRange(InputElement):
    _default_input_type = "range"


class InputFile(InputElement):
    _default_input_type = "file"

    def __init__(self,
                 label_text: str = None,
                 help_text: str = None,
                 floating_label: bool = False,
                 placeholder: str = None,
                 input_type=None,
                 id=None,
                 parent=None):
        
        super().__init__(label_text=label_text,
                         help_text=help_text,
                         floating_label=floating_label,
                         placeholder=placeholder,
                         input_type=input_type,
                         id=id,
                         parent=parent)
        
        self._files = {}
        self._input.onchange = self._load_file
        self._on_file_change = None


    def _load_file(self, *args):
        async def read_file(event, f):
                        
            # FIXME: i think i am doing things too complicated here,
            # but my understanding of loading raw bytes from file
            # inputs in javascript (and their pyodide interacions) is very much limited

            name = f.name

            uint8_array = Uint8Array.new(await f.arrayBuffer())
            buffer = io.BytesIO(bytearray(uint8_array))
            self._files[name] = buffer
            buffer.seek(0)
            buffer.name = name # not standardized, but works here # TODO: create base class for that purpose
            if self._on_file_change is not None:
                self._on_file_change(buffer)

        file_list = self._input.element.files.to_py()

        self._files = {}
    
        for f in file_list:
            # reader is a pyodide.JsProxy
            reader = FileReader.new()
    
            # Create a Python proxy for the callback function
            onload_event = create_proxy(lambda event, f=f: read_file(event, f))
    
            reader.onload = onload_event
    
            reader.readAsBinaryString(f)
    
        return

    @property
    def value(self):
        return self._files
    
    @property
    def onchange(self):
        return self._on_file_change
    
    @onchange.setter
    def onchange(self, value):
        self._on_file_change = value


class InputMultiFile(InputFile):

    def __init__(self,
                 label_text: str = None,
                 help_text: str = None,
                 floating_label: bool = False,
                 placeholder: str = None,
                 input_type=None,
                 id=None,
                 parent=None):
        super().__init__(label_text=label_text,
                         help_text=help_text,
                         floating_label=floating_label,
                         placeholder=placeholder,
                         input_type=input_type,
                         id=id,
                         parent=parent)
        self._input.set_attribute("multiple", True, is_boolean_attribute=True)

    @property
    def value(self):
        files = []
        for i in range(self._input.element.files.length):
            files.append(self._input.element.files.item(i).name)
        return files


class InputColor(InputElement):
    _default_input_type = "color"
    _default_input_class = InputFormControlColor


class InputDatalist(InputElement):

    def __init__(self,
                 options: List[str],
                 label_text: str = None,
                 help_text: str = None,
                 floating_label: bool = False,
                 placeholder: str = None,
                 input_type=None,
                 id=None,
                 parent=None):
        super().__init__(label_text=label_text,
                         help_text=help_text,
                         floating_label=floating_label,
                         placeholder=placeholder,
                         input_type=input_type,
                         id=id,
                         parent=parent)

        self._input.type = None

        self._options = options

        self._datalist = HTML.DataList(parent=self, id=self.id+"_datalist")

        for option in options:
            HTML.Option(inner_html=option, parent=self._datalist)

        self._input.set_attribute("list", self._datalist.id)

    @property
    def options(self):
        return self._options

    @options.setter
    def options(self, value):
        self._options = value
        for c in self._datalist.children:
            c.destroy()
        for option in self._options:
            HTML.Option(inner_html=option, parent=self._datalist)


class InputSelect(InputElement):

    _default_input_class = InputFormControlSelect

    def __init__(self,
                 options: List[str],
                 label_text: str = None,
                 help_text: str = None,
                 floating_label: bool = False,
                 placeholder: str = None,
                 multiple: bool = False,
                 input_type=None,
                 id=None,
                 parent=None):
        super().__init__(label_text=label_text,
                         help_text=help_text,
                         floating_label=floating_label,
                         placeholder=placeholder,
                         input_type=input_type,
                         id=id,
                         parent=parent)

        self._input.type = None

        self._options = options

        self.multiple = multiple

        for option in options:
            HTML.Option(inner_html=option, parent=self._input)

    @property
    def options(self):
        return self._options

    @options.setter
    def options(self, value):
        self._options = value
        for c in self._input.children:
            c.destroy()
        for option in self._options:
            HTML.Option(inner_html=option, parent=self._input)

    @property
    def multiple(self):
        return self._input.has_attribute("multiple")

    @multiple.setter
    def multiple(self, value):
        self._input.set_attribute("multiple", value, is_boolean_attribute=True)


class InputCheckboxSingle(InputElement):

    _default_class_name: str = "form-check"
    _default_input_type = "checkbox"
    _default_input_class = InputFormControlCheckbox
    _default_label_class = InputLabelCheckbox

    def __init__(self,
                 label_text: str = None,
                 help_text: str = None,
                 floating_label: bool = False,
                 placeholder: str = None,
                 name: str = None,
                 input_type=None,
                 id=None,
                 parent=None):
        super().__init__(label_text=label_text,
                         help_text=help_text,
                         floating_label=floating_label,
                         placeholder=placeholder,
                         input_type=input_type,
                         id=id,
                         parent=parent)

        if name is not None:
            self._input.set_attribute("name", name)

    @property
    def checked(self) -> bool:
        return self._input.element.checked

    @checked.setter
    def checked(self, value: bool):
        self._input.element.checked = value

    @property
    def value(self) -> bool:
        return self.checked

    @value.setter
    def value(self, value: bool):
        self.checked = value

    @property
    def inline(self) -> bool:
        return self.has_class("inline")

    @inline.setter
    def inline(self, value: bool):
        self.set_class("inline", value)


class InputRadioSingle(InputCheckboxSingle):
    _default_input_type = "radio"


class InputSwitchSingle(InputCheckboxSingle):
    _default_class_name: str = "form-check form-switch"


class InputCheckboxGroup(BootstrapContainer):

    _default_input_class = InputCheckboxSingle

    def __init__(self,
                 options: List[str],
                 inline: bool = False,
                 id: str = None,
                 label_text: Union[str, HTML.Element] = None,
                 group_name: str = None,
                 class_name: str = None,
                 parent: HTML.Element = None,
                 inner_html: str = None,) -> None:
        super().__init__(inner_html=inner_html,
                         id=id,
                         class_name=class_name,
                         parent=parent)

        if group_name is None:
            group_name = "id-" + str(uuid.uuid4())
        if label_text is not None:
            if isinstance(label_text, str):
                label_text = HTML.Label(inner_html=label_text, parent=self)
            else:
                self.append_child(label_text)

        self._options = options
        self._option_checkboxes = {}
        self._group_name = group_name

        for option in options:
            cb = self.__class__._default_input_class(
                option, name=group_name, parent=self)
            cb.inline = inline
            self._option_checkboxes[option] = cb

    @property
    def options(self):
        return self._options

    @options.setter
    def options(self, value):
        self._options = value
        for c in self._option_checkboxes.values():
            c.destroy()
        self._option_checkboxes = {}
        for option in self._options:
            cb = self.__class__._default_input_class(
                option, name=self._group_name, parent=self)
            self._option_checkboxes[option] = cb

    @property
    def value(self) -> List[str]:
        """
        returns a list of checked options
        """

        values = []
        for option in self._options:
            if self._option_checkboxes[option].checked:
                values.append(option)
        return values

    @value.setter
    def value(self, value: List[str]):
        for option in self._options:
            self._option_checkboxes[option].checked = option in value

    @property
    def option_checkboxes(self) -> Dict[str, InputCheckboxSingle]:
        """
        returns the form elements for each option as dictionary
        """
        return self._option_checkboxes


class InputRadioGroup(InputCheckboxGroup):
    _default_input_class = InputRadioSingle


class InputSwitchGroup(InputCheckboxGroup):
    _default_input_class = InputSwitchSingle

class Form(HTML.Form, BootstrapContainer):
    pass
    # TODO: implement more Form and form validation methods