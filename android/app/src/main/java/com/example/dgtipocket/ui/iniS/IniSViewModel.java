package com.example.dgtipocket.ui.iniS;

import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;
public class IniSViewModel extends ViewModel{


    private final MutableLiveData<String> mText;

    public IniSViewModel() {
        mText = new MutableLiveData<>();
        mText.setValue("This is IniS fragment");
    }

    public LiveData<String> getText() {
        return mText;
    }
}
