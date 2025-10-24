TARGET = report.pdf

.PHONY: build clean pdf runscripts runscripts-device

# Default experiment directory
calibration_left ?= fdb93a3978fe6356741e31b98c93c68837767080
calibration_right ?= fdb93a3978fe6356741e31b98c93c68837767080
RUNID_LEFT ?= 1234
RUNID_RIGHT ?= 1235

# calibration_right ?= 32fa7be02d2d6d5812d7cb47f8c293561b74c0b5
#calibration_right ?= 41f4570fce52da0c4bbb483f6fb7d870a551df65


download-latest-two:
	@mkdir -p data
	#@[ -d data ] && rm -rf data/* || true

	@echo "Downloading latest two experiments"
	@python download.py --latest-two


download-data:
	@mkdir -p data
	#@[ -d data ] && rm -rf data/* || true

	@echo "Downloading data for experiment $(calibration_left)"
	@python download.py --hash-id $(calibration_left)

	@echo "Downloading data for experiment $(calibration_right)"
	@python download.py --hash-id $(calibration_right)


upload-data:
	@echo "Uploading data for experiment $(calibration_left)"
	@python upload.py --hash-id $(calibration_left)

	@echo "Uploading data for experiment $(calibration_right)"
	@python upload.py --hash-id $(calibration_right)

build: clean
	@mkdir -p build
	@cp src/templates/placeholder.png build/placeholder.png
	@echo "Building latex report..."
	python src/main.py \
		--calibration-left $(calibration_left) \
		--calibration-right $(calibration_right) \
		--run-left $(RUNID_LEFT) \
		--run-right $(RUNID_RIGHT) \
		--no-tomography-plot \

pdf-only: 
	@echo "Compiling LaTeX report in pdf..."
	pdflatex -output-directory=build report.tex > logs/pdflatex.log
	@cp build/report.pdf .
	@cp build/report.pdf reports/report_$(shell echo $(calibration_left) | cut -c1-10)_vs_$(shell echo $(calibration_right) | cut -c1-10)_$$(date +%d%m%Y_%H).pdf
	@cp build/report.pdf reports/latest_report.pdf	



pdf: build pdf-only
	@echo "Compiling .tex and building the .pdf"

clean:
	@echo "Cleaning build directory..."
	@rm -rf build/*




# reportmaker-build-latex: report-clean-build-directory
# 	@mkdir -p build
# 	@cp reportmaker/templates/placeholder.png build/placeholder.png
# 	@echo "Building latex report..."
# 	python src/main.py \
# 		--experiment-left $(EXPERIMENT_DIR) \
# 		--experiment-right BASELINE \
# 		--no-tomography-plot \

# # 		--data-left runcard1 \
# # 		--data-right runcard2

# reportmaker-latex-to-pdf: 
# 	@echo "Compiling LaTeX report in pdf..."
# 	pdflatex -output-directory=build report.tex > build/pdflatex.log
# 	@cp build/report.pdf .

# reportmaker-pdf: build pdf-only
# 	@echo "PDF report generated"


# reportmaker-clean-build-directory:
# 	@echo "Cleaning build directory..."
# 	@rm -rf build/*


batch-runscripts-numpy:
	@echo "Running scripts with device=numpy..."
	sbatch scripts/runscripts_numpy.sh


# Run scripts with device=nqch (add this target)
batch-runscripts-sinq20:
	@echo "Running scripts with device=sinq20..."
	sbatch scripts/runscripts_sinq20.sh

all: batch-runscripts-numpy batch-runscripts-sinq20 build pdf
