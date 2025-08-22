CXX = clang++
CXXFLAGS = -Wall

BUILD_DIR := /tmp/aoc2024
SRCS := $(wildcard day*/part*.cc)
OBJS := $(patsubst %.cc,$(BUILD_DIR)/%.o,$(SRCS))
BINS := $(patsubst %.cc,$(BUILD_DIR)/%,$(SRCS))

all: $(BINS)

objs: $(OBJS)

$(BINS): $(BUILD_DIR)/%: $(BUILD_DIR)/%.o
	$(CXX) $(CXXFLAGS) $< -o $@

$(OBJS): $(BUILD_DIR)/%.o : %.cc
	mkdir -p $(dir $@)
	# $(CXX) $(CXXFLAGS) -c $< -D INPUT_DIR='"day01/"' -o $@
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	rm -rf $(BUILD_DIR)
