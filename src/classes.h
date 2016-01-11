
#include "di_higgs/hh2bbbb/interface/BaseSelector.h"
#include "di_higgs/hh2bbbb/interface/BasicSelector.h"
#include "di_higgs/hh2bbbb/interface/Event.h"


namespace {
  struct hh4bbbb_ExtEvent {
    ExtEvent dummy0; 
    BaseSelector<ExtEvent> dummy1;
    BasicSelector<ExtEvent> dummy2;
  };
}
