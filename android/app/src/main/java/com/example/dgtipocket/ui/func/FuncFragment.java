package com.example.dgtipocket.ui.func;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;

import com.example.dgtipocket.databinding.FragmentFuncBinding;

public class FuncFragment extends Fragment{

    private FragmentFuncBinding binding;

    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        FuncViewModel FuncViewModel =
                new ViewModelProvider(this).get(FuncViewModel.class);

        binding = FragmentFuncBinding.inflate(inflater, container, false);
        View root = binding.getRoot();

        return root;
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }
}
