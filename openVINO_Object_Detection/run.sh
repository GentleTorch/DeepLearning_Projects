ssd_bin=object_detection_sample_ssd
network=model/ssd-nest/frozen_inference_graph.xml
./${ssd_bin} -i img/image3.jpg -m ${network} -d CPU 
#/home/ailab/inference_engine_samples_build/intel64/Release/
