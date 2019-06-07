python /opt/intel/computer_vision_sdk_2018.5.455/deployment_tools/model_optimizer/mo_tf.py --input_model model/ssd-nest/frozen_inference_graph.pb --output=detection_boxes,detection_scores,num_detections --tensorflow_use_custom_operations_config model/ssd-nest/ssd_v2_support.json --tensorflow_object_detection_api_pipeline_config model/ssd-nest/pipeline.config --output_dir model/ssd-nest/ --reverse_input_channels 


