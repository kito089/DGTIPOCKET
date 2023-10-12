package com.example.dgtipocket.ui.functions.agenda;

import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;
public class AgendaViewModel extends ViewModel{

    private final MutableLiveData<String> mText;

    public AgendaViewModel() {
        mText = new MutableLiveData<>();
        mText.setValue("This is Agenda fragment");
    }

    public LiveData<String> getText() {
        return mText;
    }
}
