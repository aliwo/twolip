from swagger_ui_bundle import swagger_ui_3_path
import connexion
import prance
from typing import Any, Dict
from pathlib import Path

# from libs.database.engine import set_session_destroyer


app = connexion.App(__name__, specification_dir='api/spec/', options={'swagger_path': swagger_ui_3_path})
# set_session_destroyer(app.app)


def get_bundled_specs(main_file: Path) -> Dict[str, Any]:
    parser = prance.ResolvingParser(str(main_file.absolute()),
                                    lazy = True, strict = True)
    parser.parse()
    return parser.specification


app.add_api(get_bundled_specs(Path("api/spec/main.yaml")),
            resolver = connexion.RestyResolver("cms_rest_api"))
