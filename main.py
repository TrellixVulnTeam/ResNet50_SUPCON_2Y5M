import argparse
from Model import run
import wandb


if __name__ == '__main__':
    # WANDB PARAMS
    project = "KG-NN Transfer learning Redo"
    entity = "thesis-yugansh"

    parser = argparse.ArgumentParser(description='Process options for KG-NN')
    parser.add_argument('--loss_criterion', type=str, default="SupCon",
                        choices=["SupCon", "CE"], help="Choose the loss criterion")
    parser.add_argument('--mode', type=int, default=0,
                        help="Choose if you want to 0 : pretrain, mode : Train, 2 : Test",
                        choices=[0, 1, 2])
    parser.add_argument('--batch_size', type=int, default=1024, help="Choose batch size for training")
    parser.add_argument('--model_name', type=str, help="Choose the model to evaluate")
    parser.add_argument('--learning_rate', type=float, help="Choose learning rate", default=0.5)
    parser.add_argument('--optimizer', type=str, help="Choose optimizer", default="sgd")
    parser.add_argument('--epochs', type=int, help="Number of epochs to iterate through", default=100)
    parser.add_argument('--momentum', type=float, help="Fraction of momentum", default=0.9)
    parser.add_argument('--L2_decay', type=float, help="Multiplier for L2", default=1e-04)
    parser.add_argument('--use_nestrov', type=bool, help="Whether to use Nestrov", default=True)
    parser.add_argument('--dataset_name', type=str, help="Name of the dataset you will be using", default="Mini-ImageNet")
    parser.add_argument('--use_amsgrad', type=bool, help="Whether to use AMS-GRAD variant", default=True)
    parser.add_argument('--min_lr', type=float, help="Minimum learning rate for cosine annealing", default=0.0)

    opt = parser.parse_args()

    criterion_options = dict()

    # CONFIGURATIONS USED DURING TRAINING

    criterion_options['SupCon'] = {"criterion": 'SupCon',
                                   "epochs": opt.epochs,
                                   "temperature": 0.5,
                                   "annealing": "cosine",
                                   "learning_rate": opt.learning_rate,
                                   "optimizer": "sgd",
                                   "momentum": opt.momentum,
                                   "L2_decay": opt.L2_decay,
                                   "use_nestrov": opt.use_nestrov,
                                   "min_lr": opt.min_lr,
                                   'metric': "Cosine_Sim"}

    criterion_options['CE'] = {"criterion": 'CE',
                               "epochs": opt.epochs,
                               "optimizer": "sgd",
                               "learning_rate": opt.learning_rate,
                               "annealing": "cosine",
                               "momentum": opt.momentum,
                               "L2_decay": opt.L2_decay,
                               "use_nestrov": opt.use_nestrov,
                               "min_lr": opt.min_lr,
                               'metric': 'Accuracy'}

    config = criterion_options[opt.loss_criterion]
    config['model'] = "ResNet-50"
    config['dataset'] = opt.dataset_name

    wandb.init(project=project, config=config, entity=entity)

    if opt.mode == 0:
        run.pre_training(opt, config)
    elif opt.mode == 1:
        run.linear_phase_training(opt, config)
    else:
        run.inference(opt)



