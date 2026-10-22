CXX ?= c++
CXXFLAGS ?= -std=c++17 -O2 -Wall -Wextra -pedantic
BUILD := build

.PHONY: all demo test clean

all: $(BUILD)/signal_relay $(BUILD)/deal_ledger

$(BUILD):
	mkdir -p $(BUILD)

$(BUILD)/signal_relay: cpp/signal_relay.cpp | $(BUILD)
	$(CXX) $(CXXFLAGS) $< -o $@

$(BUILD)/deal_ledger: cpp/deal_ledger.cpp | $(BUILD)
	$(CXX) $(CXXFLAGS) $< -o $@

demo: all
	python3 python/app.py score --account "Northstar Systems" --fit 88 --intent 72 --timing 60 --confidence 95

test: all
	python3 -m unittest discover -s tests -v

clean:
	rm -rf $(BUILD) python/__pycache__ tests/__pycache__
