import os
import tensorflow as tf
import tensorflow_model_analysis as tfma
import tensorflow_transform as tft
from tfx.components import CsvExampleGen, Evaluator, Pusher, ResolverNode, SchemaGen, StatisticsGen, Trainer, Transform
from tfx.components.trainer.executor import Executor
from tfx.dsl.experimental import latest_blessed_model_resolver
from tfx.orchestration.experimental.interactive.interactive_context import InteractiveContext
from tfx.proto import pusher_pb2
from tfx.proto.evaluator_pb2 import SingleSliceSpec
from tfx.types import Channel
from tfx.utils.dsl_utils import external_input

# Определение директорий
_pipeline_root = './pipeline/'
_data_root = './data/'
_module_file = './module_file.py'
_serving_model_dir = './serving_model/'
_tfma_output_dir = './tfma_output/'
_training_output_dir = './training_output/'
_temporary_dir = './temporary/'
_metadata_path = os.path.join(_pipeline_root, 'metadata.db')

# Инициализация InteractiveContext
context = InteractiveContext(pipeline_root=_pipeline_root)

# Создание канала для данных
example_gen = CsvExampleGen(input=external_input(_data_root))

# Генерация статистики и схемы данных
statistics_gen = StatisticsGen(examples=example_gen.outputs['examples'])
schema_gen = SchemaGen(statistics=statistics_gen.outputs['statistics'], infer_feature_shape=False)

# Преобразование данных
transform = Transform(
    examples=example_gen.outputs['examples'],
    schema=schema_gen.outputs['schema'],
    module_file=_module_file
)

# Обучение модели
trainer = Trainer(
    module_file=_module_file,
    custom_executor_spec=Executor,
    examples=transform.outputs['transformed_examples'],
    schema=schema_gen.outputs['schema'],
    train_args={'num_steps': 10000},
    eval_args={'num_steps': 5000},
)

# Оценка модели
resolver = ResolverNode(
    instance_name='latest_blessed_model_resolver',
    resolver_class=latest_blessed_model_resolver.LatestBlessedModelResolver,
    model=Channel(type=tf.compat.v1.saved_model.constants.ARTIFACT_TYPE_NAME),
    model_blessing=Channel(type=tf.compat.v1.string_util.BLESSING_TYPE_NAME),
)

evaluator = Evaluator(
    examples=example_gen.outputs['examples'],
    model=trainer.outputs['model'],
    feature_slicing_spec=SingleSliceSpec(),
)

# Экспорт модели
pusher = Pusher(
    model=trainer.outputs['model'],
    model_blessing=evaluator.outputs['blessing'],
    push_destination=pusher_pb2.PushDestination(
        filesystem=pusher_pb2.PushDestination.Filesystem(base_directory=_serving_model_dir)
    ),
)

# Запуск пайплайна
context.run(example_gen)
context.run(statistics_gen)
context.run(schema_gen)
context.run(transform)
context.run(trainer)
context.run(resolver)
context.run(evaluator)
context.run(pusher)

# Экспорт метрик для TensorFlow Model Analysis
evaluator.outputs['evaluation'].get()[0].uri
