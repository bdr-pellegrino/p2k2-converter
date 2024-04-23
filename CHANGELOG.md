## [1.2.0](https://github.com/bdr-pellegrino/p2k2_converter/compare/1.1.1...1.2.0) (2024-04-22)


### Features

* add support for click_rapid product ([4bfaf4a](https://github.com/bdr-pellegrino/p2k2_converter/commit/4bfaf4aa3c9c0f0c949825f265742c6565b96aa9))


### Tests

* fix parser test introducing CLICK_RAPID product ([422870b](https://github.com/bdr-pellegrino/p2k2_converter/commit/422870b04ac3b9a04e883535bb8edff0423c7ea2))

## [1.1.1](https://github.com/bdr-pellegrino/p2k2_converter/compare/1.1.0...1.1.1) (2024-04-11)


### Bug Fixes

* solve bar allocation bug ([864ce89](https://github.com/bdr-pellegrino/p2k2_converter/commit/864ce892d75767a34349a4b873a5f688e4c35697))

## [1.1.0](https://github.com/bdr-pellegrino/p2k2_converter/compare/1.0.0...1.1.0) (2024-04-08)


### Features

* add cut definition ([366a622](https://github.com/bdr-pellegrino/p2k2_converter/commit/366a62291878c04e8ea728f8b69a0f2adeceed8e))
* add labels to the cuts ([0ec7123](https://github.com/bdr-pellegrino/p2k2_converter/commit/0ec7123cce8552a742fc4b1a5e29021e59973060))
* add machining definition to moderna product ([1468898](https://github.com/bdr-pellegrino/p2k2_converter/commit/14688986c8593eefcf2f8e65151b3c378fe714ee))
* add model definition for moderna workflow ([56ba797](https://github.com/bdr-pellegrino/p2k2_converter/commit/56ba797e62f3e2c71508c033b9a64ae20eaf6422))
* add optimal distribution of cuts on the available bars ([9e9b258](https://github.com/bdr-pellegrino/p2k2_converter/commit/9e9b25870420c3e4310a876b3df8635bd6d04648))
* add translation function to moderna ([3ce8744](https://github.com/bdr-pellegrino/p2k2_converter/commit/3ce8744b809cbfa39ca714f9257cf0425d036b54))
* add verse field to machining class ([72de9da](https://github.com/bdr-pellegrino/p2k2_converter/commit/72de9da4beb48fa30efb754ae61292c57e374e89))
* **close:** refactor machining definition ([0514fd3](https://github.com/bdr-pellegrino/p2k2_converter/commit/0514fd37bd379e4e8e4188275020a979d119b835))
* define TranslationUnit class ([4c39e8e](https://github.com/bdr-pellegrino/p2k2_converter/commit/4c39e8ef80e1b02b12d95ef3c52100ea046bf0dc))
* insert translation step in the workflow strategy ([6726c0d](https://github.com/bdr-pellegrino/p2k2_converter/commit/6726c0d8fe4ce0c3e79bea55aa5c270ab13c6caa))
* Is possible to specify a column in the excel file that signal if some  pieces are already in stock ([f43e242](https://github.com/bdr-pellegrino/p2k2_converter/commit/f43e24254e14aaa3ad1b159fde0f8084f791d289))
* parser will now determine the number of bars needed for producing the order ([cc6375e](https://github.com/bdr-pellegrino/p2k2_converter/commit/cc6375ee8b607f1ead84bab7af990cb4c2b3e77e))


### Bug Fixes

* change angle cut of moderna products from 0 to 90 ([f1c1b74](https://github.com/bdr-pellegrino/p2k2_converter/commit/f1c1b749bc65e22f09360e112f6448d219238aa4))
* fix bar labeling ([92891c5](https://github.com/bdr-pellegrino/p2k2_converter/commit/92891c58dd66da9de9121a687a1b6965ecc75411))
* fix creation of bars in the translation phase ([d6bad8d](https://github.com/bdr-pellegrino/p2k2_converter/commit/d6bad8dcd46a51e5a086c0c48b957dc5275e6066))
* fixed allocation of machining in cuts ([468f6c3](https://github.com/bdr-pellegrino/p2k2_converter/commit/468f6c314cf405eec0c8ed323c481b69d39abc8e))


### Documentation

* add comments on builder classes ([bde84bf](https://github.com/bdr-pellegrino/p2k2_converter/commit/bde84bfc3fafd790f465430496ba0217576e390b))


### Tests

* refactor close_workflow tests ([797d0ff](https://github.com/bdr-pellegrino/p2k2_converter/commit/797d0fffa66976b1ad370d909403936589285cb2))
* refactor of test_machining_definition in close workflow test ([50694ef](https://github.com/bdr-pellegrino/p2k2_converter/commit/50694efb461da3d17e473f6d3490d64dc11a8a9d))
* refactor tests ([8a35bd8](https://github.com/bdr-pellegrino/p2k2_converter/commit/8a35bd8f5aa7d23abc3db1991c12d4d356648f3e))
* separate test_parse in test_check_user_information and test_models in parser test file ([3b41625](https://github.com/bdr-pellegrino/p2k2_converter/commit/3b416254dddbf008aa1dd2e43f5a79be588b57c6))


### Build and continuous integration

* disable @semantic-release/exec ([3d29341](https://github.com/bdr-pellegrino/p2k2_converter/commit/3d29341884ec7e5672ee5f2797ab9016845f6afb))


### General maintenance

* prepare test files for moderna files ([775ac32](https://github.com/bdr-pellegrino/p2k2_converter/commit/775ac32c616582ae397442004df45501708d3ade))


### Refactoring

* automatic workflow class instantiation ([3264109](https://github.com/bdr-pellegrino/p2k2_converter/commit/3264109023883e84d7693f6a71fd05a732ec49d1))
* change data structure for passing bar quantity and length ([dd673af](https://github.com/bdr-pellegrino/p2k2_converter/commit/dd673af22a0a6d35f75f293de173938b6b518415))
* handling refinement ([ef8e00d](https://github.com/bdr-pellegrino/p2k2_converter/commit/ef8e00d3f2d34f73aaeed41e828488be140f1452))
* include moderna machinings for "CERNIERA TUBOLARE", "CERNIERA APERTA" and "H" ([1c5c238](https://github.com/bdr-pellegrino/p2k2_converter/commit/1c5c238a9c64261302a9592c166b2c5feb20a888))
* moving translation functions from translator class to __init__.py in translation package ([51e7f34](https://github.com/bdr-pellegrino/p2k2_converter/commit/51e7f341d50aa559838332203e3414f13aabcd51))
* refactor p2k2_translation method ([a0c8832](https://github.com/bdr-pellegrino/p2k2_converter/commit/a0c88323a8ce8f93f8b74e5a1dc2a7b100ec3568))
* refactoring of the translation_definition method in close workflow file ([a466c1f](https://github.com/bdr-pellegrino/p2k2_converter/commit/a466c1fb442ac966b655ac54bf4b8447b8c58c6d))
* remove Bar classes from core_classes package ([204c4c2](https://github.com/bdr-pellegrino/p2k2_converter/commit/204c4c2f2484b50d05ab242f0617d1394531a53b))

## 1.0.0 (2024-02-20)


### Features

* add bars_definition for close product ([2dbd0db](https://github.com/bdr-pellegrino/p2k2_converter/commit/2dbd0dba52cbf0b054d81891886a5e46254fcce4))
* add base implementation for data_extractor.py ([fa0a8ec](https://github.com/bdr-pellegrino/p2k2_converter/commit/fa0a8ecb7c9455d0c477a3e8b9e223bfd86ad2fa))
* add base source and step files ([1a673d1](https://github.com/bdr-pellegrino/p2k2_converter/commit/1a673d1c9584a451af39162dca7dafac69ff2b9f))
* add branch builder ([fa98e0b](https://github.com/bdr-pellegrino/p2k2_converter/commit/fa98e0b05140caae50c5b3d5188e06b7f39b7646))
* add builders interfaces ([faee664](https://github.com/bdr-pellegrino/p2k2_converter/commit/faee6645b4686ba5416ff4a528beb07e72724bc3))
* add model_definition for close product ([5b8dd30](https://github.com/bdr-pellegrino/p2k2_converter/commit/5b8dd3026b892e6ddc38f31e5297265abe4d1ae1))
* add pipeline class base implementation ([261faab](https://github.com/bdr-pellegrino/p2k2_converter/commit/261faabd319149903c1355e25574ce00fc38eec9))
* add profiles_definition for close product ([b79e9ba](https://github.com/bdr-pellegrino/p2k2_converter/commit/b79e9ba67889cdf3c594302f3bea56f39c5f66b3))
* add renaming script ([ed33dbc](https://github.com/bdr-pellegrino/p2k2_converter/commit/ed33dbc03a68a605e6df7a9465c6985ec9d1e130))
* add translator ([8aed98c](https://github.com/bdr-pellegrino/p2k2_converter/commit/8aed98ce36d31ab0d778a03cb04abc4cd28ef928))
* add workflow strategy ([06e0148](https://github.com/bdr-pellegrino/p2k2_converter/commit/06e01486e6ee55f7d70b7da49d6953d3c4942c9c))
* add workflow_strategy class ([4474c16](https://github.com/bdr-pellegrino/p2k2_converter/commit/4474c166669c5c05e262de6e8603a39b65909be2))
* add xsd file ([305af54](https://github.com/bdr-pellegrino/p2k2_converter/commit/305af5469302827e15a92026569c2ad654e7e0f6))
* add_from_lambda method in branch_builder ([3785120](https://github.com/bdr-pellegrino/p2k2_converter/commit/3785120cac6210c128f4406e05c20d7f40b123cb))
* **branch:** add get_data function in branch.py ([e1d1e0f](https://github.com/bdr-pellegrino/p2k2_converter/commit/e1d1e0ff2b2d5d7affdd1944bdeb40fed3a36832))
* build parser ([6d1b65a](https://github.com/bdr-pellegrino/p2k2_converter/commit/6d1b65a35cf626f1d85c24f9704788c16db1c7f8))
* **core:** add getter and setter methods on the data classes ([f4a0d92](https://github.com/bdr-pellegrino/p2k2_converter/commit/f4a0d92d8cab61c2a9182480e270ccaba7caeb43))
* **core:** insert core classes skeletons ([a55a00d](https://github.com/bdr-pellegrino/p2k2_converter/commit/a55a00d2785dc4b90e47a3a564d95ed970b5467c))
* first commit ([6ddc082](https://github.com/bdr-pellegrino/p2k2_converter/commit/6ddc08296facfe64fe912fcd00a255adb2806193))
* implement cut builder ([ee658cc](https://github.com/bdr-pellegrino/p2k2_converter/commit/ee658cc2c2023a48f24db7cfaac0a1244cc549bf))
* implement execute method of Branch class ([74058f6](https://github.com/bdr-pellegrino/p2k2_converter/commit/74058f6c8679db9a55a24f62bc7fc741e564dd47))
* implement first version of branch ([b5796cb](https://github.com/bdr-pellegrino/p2k2_converter/commit/b5796cb02ab27eca47357ab71a58b1be0b8367ba))
* initialize argparse ([1c7fa07](https://github.com/bdr-pellegrino/p2k2_converter/commit/1c7fa070cf59112224435487043b864dca01b940))
* **parse:** add parse function ([0916d73](https://github.com/bdr-pellegrino/p2k2_converter/commit/0916d7326ce5a64a7e7a7245c650bcc1efe401f2))
* **parser:** develop close workflow definition ([6c329ca](https://github.com/bdr-pellegrino/p2k2_converter/commit/6c329cad3ae4bbd4fc48322bda91776b3c9d91c9))
* **pipeline:** implement add_branch function ([710df82](https://github.com/bdr-pellegrino/p2k2_converter/commit/710df82cec0489d1a788e5814fa6cae9ef85b91d))
* **pipeline:** implement XlsmSource ([3dfd07f](https://github.com/bdr-pellegrino/p2k2_converter/commit/3dfd07f15dc9d1d4dde48aa169a831ff7c234968))


### Dependency updates

* **deps:** install openpyxl ([ef5a061](https://github.com/bdr-pellegrino/p2k2_converter/commit/ef5a061cb9fd0603fdf8968ecc586afd729ddc55))
* **deps:** node 18.18 ([73eec49](https://github.com/bdr-pellegrino/p2k2_converter/commit/73eec49c6fc53fe3158a0b94be99dcaf6eb328eb))
* **deps:** update dependencies ([0be2f8d](https://github.com/bdr-pellegrino/p2k2_converter/commit/0be2f8deb9b8218e509ea0926ceeb78a7a2baa70))
* **deps:** update dependency pandas to v2.1.2 ([8fe0d36](https://github.com/bdr-pellegrino/p2k2_converter/commit/8fe0d36a83c74ff23c059735a69f91ebef4904f3))
* **deps:** update dependency pandas to v2.1.3 ([27eb2b6](https://github.com/bdr-pellegrino/p2k2_converter/commit/27eb2b6e5cd7bdac497412095bdd71ee8bc9f12c))
* **deps:** update dependency pandas to v2.1.4 ([cd2b1d4](https://github.com/bdr-pellegrino/p2k2_converter/commit/cd2b1d4c3d22d352a89d57794402df9c8779b5c6))
* **deps:** update dependency pandas to v2.2.0 ([b8df6b1](https://github.com/bdr-pellegrino/p2k2_converter/commit/b8df6b14bdb94a9e4d290a67ae9090227da61d29))
* **deps:** update dependency scikit-learn to v1.3.2 ([fe7eea2](https://github.com/bdr-pellegrino/p2k2_converter/commit/fe7eea22d078a77ed77477a78785c387953888f8))
* **deps:** update dependency scikit-learn to v1.4.0 ([85de0ed](https://github.com/bdr-pellegrino/p2k2_converter/commit/85de0ed24d38277ea86a7ac71781631c097e8aaf))
* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.69 ([fa07343](https://github.com/bdr-pellegrino/p2k2_converter/commit/fa07343c199db9cf3a0784abdf1858983f80392c))
* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.70 ([2f7eb9b](https://github.com/bdr-pellegrino/p2k2_converter/commit/2f7eb9b20f5fc44a154c18cdf4ddb413da9819fc))
* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.71 ([e7efd4f](https://github.com/bdr-pellegrino/p2k2_converter/commit/e7efd4f39ac7396621ae9a7182c42975d8756476))
* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.72 ([17cd38c](https://github.com/bdr-pellegrino/p2k2_converter/commit/17cd38c5f6969e7be37be61087c63047d462e00a))
* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.73 ([ceba297](https://github.com/bdr-pellegrino/p2k2_converter/commit/ceba297fb66930fa41cfcc36794f37b16d041c60))
* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.74 ([a7c030d](https://github.com/bdr-pellegrino/p2k2_converter/commit/a7c030de41394700cc0cec89358e59a3709377b2))
* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.75 ([21e6b9a](https://github.com/bdr-pellegrino/p2k2_converter/commit/21e6b9af441d069af6c13ccbd55bad63d4a9a841))
* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.76 ([fcf51ce](https://github.com/bdr-pellegrino/p2k2_converter/commit/fcf51ce4d1048739ca4933ef56cefe69b1f25bb9))
* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.77 ([24c1ad5](https://github.com/bdr-pellegrino/p2k2_converter/commit/24c1ad5c7c2a6df6f8519c4bd3bfd9892cac7bdd))
* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.78 ([4881854](https://github.com/bdr-pellegrino/p2k2_converter/commit/488185409ad1263b83838fba5b07136517c9fe52))
* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.79 ([b09d25f](https://github.com/bdr-pellegrino/p2k2_converter/commit/b09d25f30d81f9bc22cee76f3cf2fe72e1589e62))
* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.80 ([d9e55c5](https://github.com/bdr-pellegrino/p2k2_converter/commit/d9e55c51fa21cf880450cbeee619cca167e55cec))
* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.81 ([d2608f8](https://github.com/bdr-pellegrino/p2k2_converter/commit/d2608f87dc1bb2554c4db8bd8fe57fb75512efdb))
* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.82 ([22b0719](https://github.com/bdr-pellegrino/p2k2_converter/commit/22b0719f19296441890e9e6f122df45efd5e095e))
* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.83 ([8f2ec20](https://github.com/bdr-pellegrino/p2k2_converter/commit/8f2ec20935428b99b28d412040689e56fa30a07e))
* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.84 ([cb92e70](https://github.com/bdr-pellegrino/p2k2_converter/commit/cb92e703568dbf402c51434c510fd97cb6946c52))
* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.85 ([f05865d](https://github.com/bdr-pellegrino/p2k2_converter/commit/f05865d98e638d8c7192bfdb360898b7152400f9))
* **deps:** update node.js to 20.10 ([f393b2a](https://github.com/bdr-pellegrino/p2k2_converter/commit/f393b2a2fb2d3aa98b5c5a969ef4df442d5c79de))
* **deps:** update node.js to 20.11 ([63410da](https://github.com/bdr-pellegrino/p2k2_converter/commit/63410da68d5122d155caac39b6f99de19d619825))
* **deps:** update node.js to 20.9 ([d107ca2](https://github.com/bdr-pellegrino/p2k2_converter/commit/d107ca20dd8414ef39ab6b6b95740b3ae2c75f16))
* **deps:** update node.js to v20 ([61b7e25](https://github.com/bdr-pellegrino/p2k2_converter/commit/61b7e250a9afe02465f435c6b709b2fcc872e338))
* **deps:** update python docker tag to v3.11.6 ([199ffe6](https://github.com/bdr-pellegrino/p2k2_converter/commit/199ffe6a498c6b26d358d97ac2ef7046da68e268))
* **deps:** update python docker tag to v3.12.0 ([b123d48](https://github.com/bdr-pellegrino/p2k2_converter/commit/b123d4847e25cc94e86faf1f5ec37a4e0b54e46d))
* **deps:** update python docker tag to v3.12.1 ([ac01a01](https://github.com/bdr-pellegrino/p2k2_converter/commit/ac01a014b54008d5c7af4916880413ba864f9a33))


### Bug Fixes

* change imports on tests ([4b984d2](https://github.com/bdr-pellegrino/p2k2_converter/commit/4b984d25cfff1807e31e155753b658dcecff013e))
* change values range for CERNIERA FORO ANTA machining ([11d63eb](https://github.com/bdr-pellegrino/p2k2_converter/commit/11d63eb2c626078f60add30d25011c69a2074d7a))
* **ci:** change sed path on 'Change default logging level' step ([d3e432d](https://github.com/bdr-pellegrino/p2k2_converter/commit/d3e432d65c1f42804eee07258021cf023397aa23))
* readme ([f12fb0b](https://github.com/bdr-pellegrino/p2k2_converter/commit/f12fb0b17c08a18a7e145199234dc38d43fd0ddb))
* release workflow ([9c84ec1](https://github.com/bdr-pellegrino/p2k2_converter/commit/9c84ec1497a1f8c6c438a248107746df0fa7c612))
* **release:** include .python-version in MANIFEST.in ([9d794fa](https://github.com/bdr-pellegrino/p2k2_converter/commit/9d794faac19b032c5a0f149c3e5e44df018db17b))
* renovate configuration ([0db8978](https://github.com/bdr-pellegrino/p2k2_converter/commit/0db89788ad8bef935fa97b77e7fa05aca749da28))


### Tests

* add source testing ([1146ac3](https://github.com/bdr-pellegrino/p2k2_converter/commit/1146ac3861130813d6b7f3ea6cd5c2d077e0d8d7))
* add source testing ([d354793](https://github.com/bdr-pellegrino/p2k2_converter/commit/d354793029ddf17e27ef06dbc1a16514472e3244))
* add test for cut builder ([07502af](https://github.com/bdr-pellegrino/p2k2_converter/commit/07502af3ce4ecc398ed45b390eb2553d66e001f1))
* create test for bar builder ([1feb610](https://github.com/bdr-pellegrino/p2k2_converter/commit/1feb610573a1b9db0e2599b84383ad798597651d))
* edit close.xlsm file on test folders ([1510175](https://github.com/bdr-pellegrino/p2k2_converter/commit/15101755110b6925ed480e218f527fc043840d33))
* implement tests for the translator ([45896c1](https://github.com/bdr-pellegrino/p2k2_converter/commit/45896c16e55a7ce5946bcacb9e371e2757ad7cb3))
* **pipeline:** add test for getting branch results and execution ([895d253](https://github.com/bdr-pellegrino/p2k2_converter/commit/895d253380a642de3297958362e60d6475482197))
* refactor test classes ([5b0f63f](https://github.com/bdr-pellegrino/p2k2_converter/commit/5b0f63fe2207bd754b2b69a110ccba3bd4b722da))
* refactor test using paths instead of strings to handle data ([3429a2f](https://github.com/bdr-pellegrino/p2k2_converter/commit/3429a2f61356f4a1cd05f143e2c7291f49edbf25))
* refactor test_source with temp directories ([df1a815](https://github.com/bdr-pellegrino/p2k2_converter/commit/df1a8152c22ba3b549bcbc36b08ca36cd5f97037))
* **step:** write test for step classes ([88650e7](https://github.com/bdr-pellegrino/p2k2_converter/commit/88650e73d73aa15324ea92b68c043506c25212ab))


### Build and continuous integration

* **deps:** update actions/setup-node action to v4 ([45c9acd](https://github.com/bdr-pellegrino/p2k2_converter/commit/45c9acdfed764240e4e150e65a4507205537a16a))
* **deps:** update actions/setup-python action to v5 ([66921e3](https://github.com/bdr-pellegrino/p2k2_converter/commit/66921e3580f3223689adf1665a323befbd9b3272))
* edit actions/checkout@v4 step adding token ([ee1984f](https://github.com/bdr-pellegrino/p2k2_converter/commit/ee1984f2490651bae13087d9334d88854777fb25))
* enable semantic release ([648759b](https://github.com/bdr-pellegrino/p2k2_converter/commit/648759ba41fda0cad343493709a57bcb908f7229))
* fix release by installing correct version of node ([d809f17](https://github.com/bdr-pellegrino/p2k2_converter/commit/d809f17fc96c7295e0ec526161a56f558d49aa47))


### General maintenance

* **ci:** dry run release on testpypi for template project ([b90a25a](https://github.com/bdr-pellegrino/p2k2_converter/commit/b90a25a0f1f439e0bf548eec0bfae21b1f8c44b1))
* **ci:** use jq to parse package.json ([66af494](https://github.com/bdr-pellegrino/p2k2_converter/commit/66af494bc406d4b9b649153f910016cceb1b63ce))
* init core module ([4e93753](https://github.com/bdr-pellegrino/p2k2_converter/commit/4e93753718aa3a2dee3e926123d45e27b119f716))
* initial todo-list ([154e024](https://github.com/bdr-pellegrino/p2k2_converter/commit/154e024ac1bb8a1f1c99826ab2ed6a28e703a513))
* **init:** initialize project ([8b4b055](https://github.com/bdr-pellegrino/p2k2_converter/commit/8b4b05546d1790efbe9306792274dd3ab56cf9d7))
* prepare generation example ([189fdff](https://github.com/bdr-pellegrino/p2k2_converter/commit/189fdffa1651d1be0c1cdc955812cf3dce581337))
* **release:** 1.0.0 [skip ci] ([d3b0c79](https://github.com/bdr-pellegrino/p2k2_converter/commit/d3b0c791fdf4d93194e560c1f6a6cc40736a34d8))
* **release:** 1.0.1 [skip ci] ([903a69e](https://github.com/bdr-pellegrino/p2k2_converter/commit/903a69e21c365754ca9d83e8d2797e1ceb602757))
* **release:** simplify renovate conf ([23da9b6](https://github.com/bdr-pellegrino/p2k2_converter/commit/23da9b61d38adbe974c53240f05fb71ea685fb03))
* remove useless Dockerfile ([0272af7](https://github.com/bdr-pellegrino/p2k2_converter/commit/0272af71647e254f7622d38ace6000f0cbc7f17d))
* removed .pyi files ([30618b4](https://github.com/bdr-pellegrino/p2k2_converter/commit/30618b43ee78ef8cc0acd39c9a42e4856d8ce566))
* solve conflicts ([16f39f5](https://github.com/bdr-pellegrino/p2k2_converter/commit/16f39f5263f6ae3587f3c02419fad1975b6367dd))
* write some instructions ([7da9554](https://github.com/bdr-pellegrino/p2k2_converter/commit/7da9554a6e458c5fc253a222b295fbeb6a7862ec))


### Style improvements

* ordered classes spaces ([05855dd](https://github.com/bdr-pellegrino/p2k2_converter/commit/05855ddbd7b855e14f8cc88c0ed56322fda23cd6))


### Refactoring

* add checks to input parameters ([ccca421](https://github.com/bdr-pellegrino/p2k2_converter/commit/ccca421b43f6c96c9bec3ae68b8fb1f484a339ca))
* add type support for branch class ([748112e](https://github.com/bdr-pellegrino/p2k2_converter/commit/748112ec0c6715f35458115ce2b0386f00d88aa0))
* change package import  in test_parser from data to test.data ([68ee8b8](https://github.com/bdr-pellegrino/p2k2_converter/commit/68ee8b8d7e9ef05ea23718c289cca190d0c63c2b))
* improvement of imports for the source and step models ([e1a8945](https://github.com/bdr-pellegrino/p2k2_converter/commit/e1a8945ae42f8cf5541272d110f7f1ee29ecb2d9))
* now base classes are defined as abstract ([d751339](https://github.com/bdr-pellegrino/p2k2_converter/commit/d751339c3e69c2c53804833b3f06013c48fe13a5))
* **workflow:** add total length ([b870df4](https://github.com/bdr-pellegrino/p2k2_converter/commit/b870df4974a3d2861cfbe6f10d89e82b79e263a7))
* xlsm_source handle error ([fad6668](https://github.com/bdr-pellegrino/p2k2_converter/commit/fad6668139160e97926417194ad51b0f7c431371))

## [1.0.1](https://github.com/aequitas-aod/template-python-project/compare/1.0.0...1.0.1) (2024-02-02)


### Dependency updates

* **deps:** update dependency pandas to v2.1.2 ([8fe0d36](https://github.com/aequitas-aod/template-python-project/commit/8fe0d36a83c74ff23c059735a69f91ebef4904f3))
* **deps:** update dependency pandas to v2.1.3 ([27eb2b6](https://github.com/aequitas-aod/template-python-project/commit/27eb2b6e5cd7bdac497412095bdd71ee8bc9f12c))
* **deps:** update dependency pandas to v2.1.4 ([cd2b1d4](https://github.com/aequitas-aod/template-python-project/commit/cd2b1d4c3d22d352a89d57794402df9c8779b5c6))
* **deps:** update dependency pandas to v2.2.0 ([b8df6b1](https://github.com/aequitas-aod/template-python-project/commit/b8df6b14bdb94a9e4d290a67ae9090227da61d29))
* **deps:** update dependency scikit-learn to v1.3.2 ([fe7eea2](https://github.com/aequitas-aod/template-python-project/commit/fe7eea22d078a77ed77477a78785c387953888f8))
* **deps:** update dependency scikit-learn to v1.4.0 ([85de0ed](https://github.com/aequitas-aod/template-python-project/commit/85de0ed24d38277ea86a7ac71781631c097e8aaf))
* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.69 ([fa07343](https://github.com/aequitas-aod/template-python-project/commit/fa07343c199db9cf3a0784abdf1858983f80392c))
* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.70 ([2f7eb9b](https://github.com/aequitas-aod/template-python-project/commit/2f7eb9b20f5fc44a154c18cdf4ddb413da9819fc))
* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.71 ([e7efd4f](https://github.com/aequitas-aod/template-python-project/commit/e7efd4f39ac7396621ae9a7182c42975d8756476))
* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.72 ([17cd38c](https://github.com/aequitas-aod/template-python-project/commit/17cd38c5f6969e7be37be61087c63047d462e00a))
* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.73 ([ceba297](https://github.com/aequitas-aod/template-python-project/commit/ceba297fb66930fa41cfcc36794f37b16d041c60))
* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.74 ([a7c030d](https://github.com/aequitas-aod/template-python-project/commit/a7c030de41394700cc0cec89358e59a3709377b2))
* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.75 ([21e6b9a](https://github.com/aequitas-aod/template-python-project/commit/21e6b9af441d069af6c13ccbd55bad63d4a9a841))
* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.76 ([fcf51ce](https://github.com/aequitas-aod/template-python-project/commit/fcf51ce4d1048739ca4933ef56cefe69b1f25bb9))
* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.77 ([24c1ad5](https://github.com/aequitas-aod/template-python-project/commit/24c1ad5c7c2a6df6f8519c4bd3bfd9892cac7bdd))
* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.78 ([4881854](https://github.com/aequitas-aod/template-python-project/commit/488185409ad1263b83838fba5b07136517c9fe52))
* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.79 ([b09d25f](https://github.com/aequitas-aod/template-python-project/commit/b09d25f30d81f9bc22cee76f3cf2fe72e1589e62))
* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.80 ([d9e55c5](https://github.com/aequitas-aod/template-python-project/commit/d9e55c51fa21cf880450cbeee619cca167e55cec))
* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.81 ([d2608f8](https://github.com/aequitas-aod/template-python-project/commit/d2608f87dc1bb2554c4db8bd8fe57fb75512efdb))
* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.82 ([22b0719](https://github.com/aequitas-aod/template-python-project/commit/22b0719f19296441890e9e6f122df45efd5e095e))
* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.83 ([8f2ec20](https://github.com/aequitas-aod/template-python-project/commit/8f2ec20935428b99b28d412040689e56fa30a07e))
* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.84 ([cb92e70](https://github.com/aequitas-aod/template-python-project/commit/cb92e703568dbf402c51434c510fd97cb6946c52))
* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.85 ([f05865d](https://github.com/aequitas-aod/template-python-project/commit/f05865d98e638d8c7192bfdb360898b7152400f9))
* **deps:** update node.js to 20.10 ([f393b2a](https://github.com/aequitas-aod/template-python-project/commit/f393b2a2fb2d3aa98b5c5a969ef4df442d5c79de))
* **deps:** update node.js to 20.11 ([63410da](https://github.com/aequitas-aod/template-python-project/commit/63410da68d5122d155caac39b6f99de19d619825))
* **deps:** update node.js to 20.9 ([d107ca2](https://github.com/aequitas-aod/template-python-project/commit/d107ca20dd8414ef39ab6b6b95740b3ae2c75f16))
* **deps:** update node.js to v20 ([61b7e25](https://github.com/aequitas-aod/template-python-project/commit/61b7e250a9afe02465f435c6b709b2fcc872e338))
* **deps:** update python docker tag to v3.12.0 ([b123d48](https://github.com/aequitas-aod/template-python-project/commit/b123d4847e25cc94e86faf1f5ec37a4e0b54e46d))
* **deps:** update python docker tag to v3.12.1 ([ac01a01](https://github.com/aequitas-aod/template-python-project/commit/ac01a014b54008d5c7af4916880413ba864f9a33))


### Bug Fixes

* **release:** include .python-version in MANIFEST.in ([9d794fa](https://github.com/aequitas-aod/template-python-project/commit/9d794faac19b032c5a0f149c3e5e44df018db17b))


### Build and continuous integration

* **deps:** update actions/setup-node action to v4 ([45c9acd](https://github.com/aequitas-aod/template-python-project/commit/45c9acdfed764240e4e150e65a4507205537a16a))
* **deps:** update actions/setup-python action to v5 ([66921e3](https://github.com/aequitas-aod/template-python-project/commit/66921e3580f3223689adf1665a323befbd9b3272))

## 1.0.0 (2023-10-12)


### Features

* add renaming script ([ed33dbc](https://github.com/aequitas-aod/template-python-project/commit/ed33dbc03a68a605e6df7a9465c6985ec9d1e130))
* first commit ([6ddc082](https://github.com/aequitas-aod/template-python-project/commit/6ddc08296facfe64fe912fcd00a255adb2806193))


### Dependency updates

* **deps:** node 18.18 ([73eec49](https://github.com/aequitas-aod/template-python-project/commit/73eec49c6fc53fe3158a0b94be99dcaf6eb328eb))
* **deps:** update dependencies ([0be2f8d](https://github.com/aequitas-aod/template-python-project/commit/0be2f8deb9b8218e509ea0926ceeb78a7a2baa70))
* **deps:** update python docker tag to v3.11.6 ([199ffe6](https://github.com/aequitas-aod/template-python-project/commit/199ffe6a498c6b26d358d97ac2ef7046da68e268))


### Bug Fixes

* readme ([f12fb0b](https://github.com/aequitas-aod/template-python-project/commit/f12fb0b17c08a18a7e145199234dc38d43fd0ddb))
* release workflow ([9c84ec1](https://github.com/aequitas-aod/template-python-project/commit/9c84ec1497a1f8c6c438a248107746df0fa7c612))
* renovate configuration ([0db8978](https://github.com/aequitas-aod/template-python-project/commit/0db89788ad8bef935fa97b77e7fa05aca749da28))


### Build and continuous integration

* enable semantic release ([648759b](https://github.com/aequitas-aod/template-python-project/commit/648759ba41fda0cad343493709a57bcb908f7229))
* fix release by installing correct version of node ([d809f17](https://github.com/aequitas-aod/template-python-project/commit/d809f17fc96c7295e0ec526161a56f558d49aa47))


### General maintenance

* **ci:** dry run release on testpypi for template project ([b90a25a](https://github.com/aequitas-aod/template-python-project/commit/b90a25a0f1f439e0bf548eec0bfae21b1f8c44b1))
* **ci:** use jq to parse package.json ([66af494](https://github.com/aequitas-aod/template-python-project/commit/66af494bc406d4b9b649153f910016cceb1b63ce))
* initial todo-list ([154e024](https://github.com/aequitas-aod/template-python-project/commit/154e024ac1bb8a1f1c99826ab2ed6a28e703a513))
* remove useless Dockerfile ([0272af7](https://github.com/aequitas-aod/template-python-project/commit/0272af71647e254f7622d38ace6000f0cbc7f17d))
* write some instructions ([7da9554](https://github.com/aequitas-aod/template-python-project/commit/7da9554a6e458c5fc253a222b295fbeb6a7862ec))
