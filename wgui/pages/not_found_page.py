import dash
import dash_mantine_components as dmc


def not_found_page(location):
    not_found_page = dmc.Stack(
        [
            dmc.Text(
                "404: Not found",
                c="red",
                style={"fontSize": 40},
            ),
            dmc.Text(
                f"Страницы {location} вроде нет. Как ты сюда попал?",
                size="xl",
            ),
        ],
        gap="md",
    )

    return (
        False,
        not_found_page,
    )
