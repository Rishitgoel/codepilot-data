# CodePilot Premium Problems CDN & Open Dataset

[![jsDelivr Hits](https://data.jsdelivr.com/v1/package/gh/Rishitgoel/codepilot-data/badge)](https://www.jsdelivr.com/package/gh/Rishitgoel/codepilot-data)
[![Total Problems](https://img.shields.io/badge/problems-52-brightgreen)](index.json)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

This repository serves as the high-speed Global Edge CDN for **[CodePilot](https://github.com/Rishitgoel/CodePilot)** (LeetCode, GFG & Codeforces Assistant). It provides structured algorithmic problem formulations, clean starter boilerplate templates, standard test cases, hints, and 1:1 free mirror platform links.

---

## ⚡ High-Speed Global Edge CDN Endpoints

All files are delivered through **jsDelivr Global Edge CDN** (backed by Cloudflare, Fastly, and GCore) with HTTP/2, Brotli compression, zero rate limits, and 15–35ms global latency.

### 1. Fetch Problem by Slug
```http
GET https://cdn.jsdelivr.net/gh/Rishitgoel/codepilot-data@main/problems/{slug}.json
```
*Example:*
`https://cdn.jsdelivr.net/gh/Rishitgoel/codepilot-data@main/problems/meeting-rooms-ii.json`

### 2. Fetch Full Manifest Index
```http
GET https://cdn.jsdelivr.net/gh/Rishitgoel/codepilot-data@main/index.json
```

### Fallback GitHub Raw URL
```http
GET https://raw.githubusercontent.com/Rishitgoel/codepilot-data/main/problems/{slug}.json
```

---

## 📦 JSON Schema Structure

Each `{slug}.json` strictly adheres to the following specification:

```json
{
  "id": 253,
  "slug": "meeting-rooms-ii",
  "title": "Meeting Rooms II",
  "difficulty": "Medium",
  "rating": 1680,
  "topics": ["Array", "Two Pointers", "Greedy", "Sorting", "Heap (Priority Queue)"],
  "companies": ["Google", "Amazon", "Meta", "Bloomberg", "Microsoft", "Uber"],
  "freeMirror": {
    "platform": "LintCode",
    "id": 919,
    "url": "https://www.lintcode.com/problem/919/"
  },
  "description": "Given an array of meeting time intervals...",
  "examples": [
    {
      "input": "intervals = [[0,30],[5,10],[15,20]]",
      "output": "2",
      "explanation": "Room 1 holds [0,30]. Room 2 holds [5,10] and [15,20]."
    }
  ],
  "constraints": [
    "1 <= intervals.length <= 10^4",
    "0 <= start_i < end_i <= 10^6"
  ],
  "starterTemplates": {
    "python": "class Solution:\n    def minMeetingRooms(self, intervals: List[List[int]]) -> int:\n        pass\n",
    "cpp": "class Solution {\npublic:\n    int minMeetingRooms(vector<vector<int>>& intervals) {\n        \n    }\n};",
    "java": "class Solution {\n    public int minMeetingRooms(int[][] intervals) {\n        \n    }\n};",
    "javascript": "var minMeetingRooms = function(intervals) {\n    \n};"
  },
  "testcases": [
    { "input": "[[0,30],[5,10],[15,20]]", "expected": "2" },
    { "input": "[[7,10],[2,4]]", "expected": "1" }
  ],
  "hints": [
    "Sort the intervals by start time...",
    "Use a min-heap tracking end times..."
  ]
}
```

---

## 🛡️ Chrome Web Store Compliance & Safety
- **No Remote Code Execution**: Content is strictly static JSON data. No scripts, `eval()`, or executable blobs are delivered or executed.
- **Fair Use & Copyright Cleanliness**: Problem formulations use mathematical and algorithmic descriptions, clean open-source starter boilerplate, and links to free alternative online judges.
