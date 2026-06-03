import nemo.collections.asr as nemo_asr
import pytorch_lightning as pl


def finetune_parakeet(train_manifest, val_manifest, output_path="out/parakeet_finetuned.nemo"):
    model = nemo_asr.models.ASRModel.from_pretrained("nvidia/parakeet-tdt-0.6b-v2")

    model.setup_training_data({
        "manifest_filepath": train_manifest,
        "sample_rate": 16000,
        "batch_size": 8,
        "shuffle": True,
        "num_workers": 4,
    })
    model.setup_validation_data({
        "manifest_filepath": val_manifest,
        "sample_rate": 16000,
        "batch_size": 8,
        "shuffle": False,
        "num_workers": 4,
    })

    model.setup_optimization({
        "name": "adamw",
        "lr": 1e-4,
        "sched": {"name": "CosineAnnealing", "warmup_steps": 500}
    })

    trainer = pl.Trainer(max_epochs=10, accelerator="gpu", devices=1,
                         precision="bf16-mixed", accumulate_grad_batches=4)
    trainer.fit(model)
    model.save_to(output_path)
    return model


if __name__ == "__main__":
    finetune_parakeet("train.jsonl", "val.jsonl")
