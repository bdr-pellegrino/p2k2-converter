from .workflow_strategy import WorkflowStrategy
from .close import Close

__class_names__ = {Close}


def workflow_for_product(product_name: str, *args, **kwargs) -> WorkflowStrategy:
    """
    This function will return the correct workflow for the product name given.
    Args:
        product_name: Name of the product to get the workflow for
        *args:
        **kwargs:

    Returns:
        The workflow for the product name given
    """
    for workflow in __class_names__:
        if product_name.lower() == workflow.__name__.lower():
            return workflow(*args, **kwargs)


__all__ = ["WorkflowStrategy", "Close", "workflow_for_product"]
