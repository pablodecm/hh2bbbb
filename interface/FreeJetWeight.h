
#pragma once

#include <algorithm>

#include "TH2.h"

#include "BaseOperator.h"

template <class EventClass> class FreeJetWeight2D : public BaseOperator<EventClass> {

  public:

    std::string w_name_;
    TH2D * ratio_;
    TH2D * filler_;


    FreeJetWeight2D( const std::string w_name, TH2D * ratio ) : 
      w_name_(w_name),
      ratio_(ratio),
      filler_(new TH2D(*ratio_))  {
        filler_->Reset();
    }
    virtual ~FreeJetWeight2D() { 
      delete filler_;
    }

    virtual bool process( EventClass & ev ) {

        const auto & jet = ev.jets_.at(ev.free_is_.at(0));;
        auto g_bin = filler_->Fill(jet.pt(), std::abs(jet.eta()));
        auto weight = ratio_->GetBinContent(g_bin);
        auto weight_unc = ratio_->GetBinError(g_bin);

        ev.eventInfo_.emplaceWeight(w_name_, float(weight));
        ev.eventInfo_.emplaceWeight(w_name_+"_unc", float(weight));

      return true;
    }

    virtual std::string get_name() {
      return w_name_;
    }
};
