import pytest
import os
from montreal_forced_aligner.g2p.trainer import PyniniTrainer

from montreal_forced_aligner.g2p.generator import PyniniDictionaryGenerator

from montreal_forced_aligner.models import G2PModel

from montreal_forced_aligner import __version__


def test_training(sick_dict, sick_g2p_model_path, temp_dir):
    trainer = PyniniTrainer(sick_dict, sick_g2p_model_path, temp_directory=temp_dir)
    trainer.validate()

    trainer.train()
    model = G2PModel(sick_g2p_model_path)
    assert model.meta['version'] == __version__
    assert model.meta['architecture'] == 'pynini'
    assert model.meta['phones'] == sick_dict.nonsil_phones


def test_generator(sick_g2p_model_path, sick_corpus, g2p_sick_output):
    model = G2PModel(sick_g2p_model_path)
    gen = PyniniDictionaryGenerator(model, sick_corpus.word_set)
    gen.output(g2p_sick_output)
    assert os.path.exists(g2p_sick_output)
