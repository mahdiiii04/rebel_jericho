# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors and the HuggingFace Datasets Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint as: python3
"""REBEL"""

from __future__ import absolute_import, division, print_function

import pandas as pd

import datasets

import re 
import json
import logging
import math
from collections import defaultdict

_DESCRIPTION = """\
Jericho DATASET for relation extraction from Text based games observations 
"""

_URL = '/content/rebel_jericho/data/jericho'
_URLS = {
    "train": _URL + "train.json",
    "dev": _URL + "val.json",
    "test": _URL + "test.json",
}


class RebelConfig(datasets.BuilderConfig):
    """BuilderConfig for REBEL."""

    def __init__(self, **kwargs):
        """BuilderConfig for REBEL.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(RebelConfig, self).__init__(**kwargs)


class Rebel(datasets.GeneratorBasedBuilder):
    """Rebel 1.0"""

    BUILDER_CONFIGS = [
        RebelConfig(
            name="plain_text",
            version=datasets.Version("1.0.0", ""),
            description="Plain text",
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "title": datasets.Value("string"),
                    "context": datasets.Value("string"),
                    "triplets": datasets.Value("string"),
                }
            ),
            # No default supervised_keys (as we have to pass both question
            # and context as input).
            supervised_keys=None,
            # homepage="",
#             citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        if self.config.data_files:
            downloaded_files = {
                "train": self.config.data_files["train"], # self.config.data_dir + "en_train.jsonl",
                "dev": self.config.data_files["dev"], #self.config.data_dir + "en_val.jsonl",
                "test": self.config.data_files["test"], #self.config.data_dir + "en_test.jsonl",
            }
        else:
            downloaded_files = dl_manager.download_and_extract(_URLS)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN, 
                gen_kwargs={"filepath": downloaded_files["train"][0] if isinstance(downloaded_files["train"], list) else downloaded_files["train"]}
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION, 
                gen_kwargs={"filepath": downloaded_files["dev"][0] if isinstance(downloaded_files["dev"], list) else downloaded_files["dev"]}
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST, 
                gen_kwargs={"filepath": downloaded_files["test"][0] if isinstance(downloaded_files["test"], list) else downloaded_files["test"]}
            ),
]


    def _generate_examples(self, filepath):
        """This function returns the examples in the raw (text) form."""
        logging.info("Generating examples from = %s", filepath)

        with open(filepath, encoding="utf-8") as f:
            try:
                data = json.load(f)  # 🔥 Load the entire JSON file as a list
            except json.JSONDecodeError as e:
                print(f"❌ Error loading JSON file: {e}")
                return

            for id_, article in enumerate(data):  # 🔥 Iterate over elements, not lines
                yield str(id_), {
                    "title": "Text-Based Adventure",
                    "context": article["input"],
                    "id": str(id_),
                    "triplets": article["output"],
                }
