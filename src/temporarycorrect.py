

    # MERMIN TABLE
    try:
        context = context_mermin_table(context, cfg)
    except Exception as e:
        logging.error(f"Error preparing Mermin table: {e}")
        context["mermin_maximum"] = "N/A"
        context["mermin_maximum_right"] = "N/A"

    # # GROVER 2Q PLOTS
    # if cfg.grover2q_plot:
    #     try:
    #         context = context_grover2q_plots(context, cfg)
    #     except Exception as e:
    #         logging.error(f"Error preparing Grover 2Q plots: {e}")
    #         context["grover2q_plot_is_set"] = False
    #         context["plot_grover2q"] = "placeholder.png"
    #         context["plot_grover2q_right"] = "placeholder.png"
    #         context["grover2q_runtime_left"] = "N/A"
    #         context["grover2q_runtime_right"] = "N/A"
    #         context["grover2q_qubits_left"] = "N/A"
    #         context["grover2q_qubits_right"] = "N/A"
    # else:
    #     context["grover2q_plot_is_set"] = False

    # # GROVER 3Q PLOTS
    # if cfg.grover3q_plot:
    #     try:
    #         context = context_grover3q_plots(context, cfg)
    #     except Exception as e:
    #         logging.error(f"Error preparing Grover 3Q plots: {e}")
    #         context["grover3q_plot_is_set"] = False
    #         context["plot_grover3q"] = "placeholder.png"
    #         context["plot_grover3q_right"] = "placeholder.png"
    #         context["grover3q_description"] = "N/A"
    #         context["grover3q_runtime_left"] = "N/A"
    #         context["grover3q_runtime_right"] = "N/A"
    #         context["grover3q_qubits_left"] = "N/A"
    #         context["grover3q_qubits_right"] = "N/A"
    # else:
    #     context["grover3q_plot_is_set"] = False

    # # GHZ PLOTS
    # if cfg.ghz_plot:
    #     try:
    #         context = context_ghz_plots(context, cfg)
    #     except Exception as e:
    #         logging.error(f"Error preparing GHZ plots: {e}")
    #         context["ghz_plot_is_set"] = False
    #         context["plot_ghz"] = "placeholder.png"
    #         context["plot_ghz_right"] = "placeholder.png"
    #         context["ghz_description"] = "N/A"
    #         context["ghz_runtime_left"] = "N/A"
    #         context["ghz_runtime_right"] = "N/A"
    #         context["ghz_qubits_left"] = "N/A"
    #         context["ghz_qubits_right"] = "N/A"
    # else:
    #     logging.info("GHZ plot is not set, skipping...")
    #     context["ghz_plot_is_set"] = False

    # # PROCESS TOMOGRAPHY PLOTS
    # if cfg.process_tomography_plot:
    #     try:
    #         context = context_process_tomography_plots(context, cfg)
    #     except Exception as e:
    #         logging.error(f"Error preparing Process Tomography plots: {e}")
    #         context["process_tomography_plot_is_set"] = False
    #         context["plot_process_tomography_left"] = "placeholder.png"
    #         context["plot_process_tomography_right"] = "placeholder.png"
    #         context["process_tomography_runtime_left"] = "N/A"
    #         context["process_tomography_runtime_right"] = "N/A"
    # else:
    #     logging.info("Process Tomography plot is not set, skipping...")
    #     context["process_tomography_plot_is_set"] = False

    # TOMOGRAPHY PLOTS
    if cfg.tomography_plot:
        try:
            context = context_tomography_plots(context, cfg)
        except Exception as e:
            logging.error(f"Error preparing Tomography plots: {e}")
            context["tomography_plot_is_set"] = False
            context["plot_tomography"] = "placeholder.png"
            context["plot_tomography_right"] = "placeholder.png"
    else:
        logging.info("Tomography plot is not set, skipping...")
        context["tomography_plot_is_set"] = False

    # REUPLOADING CLASSIFIER PLOTS
    if cfg.reuploading_classifier_plot:
        try:
            context = context_reuploading_classifier_plots(context, cfg)
        except Exception as e:
            logging.error(f"Error preparing Reuploading Classifier plots: {e}")
            context["reuploading_classifier_plot_is_set"] = False
            context["plot_reuploading_classifier"] = "placeholder.png"
            context["plot_reuploading_classifier_right"] = "placeholder.png"
            context["reuploading_classifier_description"] = "N/A"
            context["reuploading_classifier_runtime_left"] = "N/A"
            context["reuploading_classifier_runtime_right"] = "N/A"
            context["reuploading_classifier_qubits_left"] = "N/A"
            context["reuploading_classifier_qubits_right"] = "N/A"
    else:
        logging.info("Reuploading Classifier plot is not set, skipping...")
        context["reuploading_classifier_plot_is_set"] = False

    # QFT PLOTS
    if cfg.qft_plot:
        try:
            context = context_qft_plots(context, cfg)
        except Exception as e:
            logging.error(f"Error preparing QFT plots: {e}")
            context["qft_plot_is_set"] = False
            context["plot_qft"] = "placeholder.png"
            context["plot_qft_right"] = "placeholder.png"
            context["qft_description"] = "N/A"
            context["qft_runtime_left"] = "N/A"
            context["qft_runtime_right"] = "N/A"
            context["qft_qubits_left"] = "N/A"
            context["qft_qubits_right"] = "N/A"
    else:
        logging.info("QFT plot is not set, skipping...")
        context["qft_plot_is_set"] = False

    # YEAST CLASSIFICATION 4Q PLOTS
    if cfg.yeast_plot_4q:
        try:
            context = context_yeast_4q_plots(context, cfg)
        except Exception as e:
            logging.error(f"Error preparing Yeast 4Q plots: {e}")
            context["yeast_classification_4q_plot_is_set"] = False
            context["plot_yeast_4q"] = "placeholder.png"
            context["plot_yeast_4q_right"] = "placeholder.png"
            context["qml_4Q_yeast_description"] = "N/A"
            context["qml_4Q_yeast_runtime_left"] = "N/A"
            context["qml_4Q_yeast_runtime_right"] = "N/A"
    else:
        logging.info("Yeast 4Q plot is not set, skipping...")
        context["yeast_classification_4q_plot_is_set"] = False

    # YEAST CLASSIFICATION 3Q PLOTS
    if cfg.yeast_plot_3q:
        try:
            context = context_yeast_3q_plots(context, cfg)
        except Exception as e:
            logging.error(f"Error preparing Yeast 3Q plots: {e}")
            context["yeast_classification_3q_plot_is_set"] = False
            context["plot_yeast_3q"] = "placeholder.png"
            context["plot_yeast_3q_right"] = "placeholder.png"
            context["yeast_3q_accuracy_left"] = "N/A"
            context["yeast_3q_accuracy_right"] = "N/A"
    else:
        logging.info("Yeast 3Q plot is not set, skipping...")
        context["yeast_classification_3q_plot_is_set"] = False

    # STATLOG CLASSIFICATION 4Q PLOTS
    if cfg.statlog_plot_4q:
        try:
            context = context_statlog_4q_plots(context, cfg)
        except Exception as e:
            logging.error(f"Error preparing StatLog 4Q plots: {e}")
            context["statlog_classification_4q_plot_is_set"] = False
            context["plot_statlog_4q"] = "placeholder.png"
            context["plot_statlog_4q_right"] = "placeholder.png"
    else:
        logging.info("StatLog 4Q plot is not set, skipping...")
        context["statlog_classification_4q_plot_is_set"] = False

    # STATLOG CLASSIFICATION 3Q PLOTS
    if cfg.statlog_plot_3q:
        try:
            context = context_statlog_3q_plots(context, cfg)
        except Exception as e:
            logging.error(f"Error preparing StatLog 3Q plots: {e}")
            context["statlog_classification_3q_plot_is_set"] = False
            context["plot_statlog_3q"] = "placeholder.png"
            context["plot_statlog_3q_right"] = "placeholder.png"
            context["statlog_3q_accuracy_left"] = "N/A"
            context["statlog_3q_accuracy_right"] = "N/A"
    else:
        logging.info("StatLog 3Q plot is not set, skipping...")
        context["statlog_classification_3q_plot_is_set"] = False

    # AMPLITUDE ENCODING PLOTS
    if cfg.amplitude_encoding_plot:
        try:
            context = context_amplitude_encoding_plots(context, cfg)
        except Exception as e:
            logging.error(f"Error preparing Amplitude Encoding plots: {e}")
            context["amplitude_encoding_plot_is_set"] = False
            context["plot_amplitude_encoding"] = "placeholder.png"
            context["plot_amplitude_encoding_right"] = "placeholder.png"
            context["amplitude_encoding_runtime_left"] = "N/A"
            context["amplitude_encoding_runtime_right"] = "N/A"
            context["amplitude_encoding_qubits_left"] = "N/A"
            context["amplitude_encoding_qubits_right"] = "N/A"
    else:
        logging.info("Amplitude Encoding plot is not set, skipping...")
        context["amplitude_encoding_plot_is_set"] = False

    return context