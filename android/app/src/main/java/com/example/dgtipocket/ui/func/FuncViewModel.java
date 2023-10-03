package com.example.dgtipocket.ui.func;

import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;

public class FuncViewModel extends ViewModel{

    private final MutableLiveData<String> mText;

    public FuncViewModel() {
        mText = new MutableLiveData<>();
        mText.setValue("This is Func fragment");
    }

    public LiveData<String> getText() {
        return mText;
    }
}
