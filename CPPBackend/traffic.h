#pragma once

// Compatibility wrapper to avoid including the Windows SDK's traffic.h.
// Existing includes of "traffic.h" in the project will now resolve to our core header.
#include "traffic_core.h"

