from typing import Union, Any
from langchain_core.messages import AnyMessage
from pydantic import BaseModel

from langgraph.prebuilt import ToolNode
from langchain_core.runnables import RunnableConfig
from langgraph.store.base import BaseStore
from langchain_core.runnables.config import (
    get_config_list,
    get_executor_for_config,
)


class CustomToolNode(ToolNode):

    def _func(
        self,
        input: Union[
            list[AnyMessage],
            dict[str, Any],
            BaseModel,
        ],
        config: RunnableConfig,
        *,
        store: BaseStore,
    ) -> Any:
        tool_calls, output_type = self._parse_input(input, store)
        tool_calls = [tool_calls[0]]
        config_list = get_config_list(config, len(tool_calls))
        with get_executor_for_config(config) as executor:
            outputs = [*executor.map(self._run_one, tool_calls, config_list)]
        # TypedDict, pydantic, dataclass, etc. should all be able to load from dict
        return outputs if output_type == "list" else {self.messages_key: outputs}
