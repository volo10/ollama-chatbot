#!/bin/bash

# Script to run all chatbot tests

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║         Ollama Chatbot - Complete Test Suite                ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track results
TOTAL_PASSED=0
TOTAL_FAILED=0

# Test v1.0
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Testing Version 1.0 (chatbot.py)${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
python3 test_chatbot_v1.py
V1_RESULT=$?

if [ $V1_RESULT -eq 0 ]; then
    echo -e "${GREEN}✅ v1.0 Tests PASSED${NC}"
    ((TOTAL_PASSED++))
else
    echo -e "${RED}❌ v1.0 Tests FAILED${NC}"
    ((TOTAL_FAILED++))
fi

echo ""

# Test v2.0
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Testing Version 2.0 (chatbot_v2.py)${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
python3 test_chatbot_v2.py
V2_RESULT=$?

if [ $V2_RESULT -eq 0 ]; then
    echo -e "${GREEN}✅ v2.0 Tests PASSED${NC}"
    ((TOTAL_PASSED++))
else
    echo -e "${RED}❌ v2.0 Tests FAILED${NC}"
    ((TOTAL_FAILED++))
fi

echo ""

# Test v3.0
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Testing Version 3.0 (chatbot_v3.py)${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
python3 test_chatbot_v3.py
V3_RESULT=$?

if [ $V3_RESULT -eq 0 ]; then
    echo -e "${GREEN}✅ v3.0 Tests PASSED${NC}"
    ((TOTAL_PASSED++))
else
    echo -e "${RED}❌ v3.0 Tests FAILED${NC}"
    ((TOTAL_FAILED++))
fi

echo ""

# Summary
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                      TEST SUMMARY                            ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "Versions Passed: $TOTAL_PASSED / 3"
echo "Versions Failed: $TOTAL_FAILED / 3"
echo ""

if [ $TOTAL_FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}⚠️  Some tests failed. Please review the output above.${NC}"
    exit 1
fi

