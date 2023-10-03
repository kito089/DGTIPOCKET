package com.example.dgtipocket.ui.iniS;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;

import com.example.dgtipocket.databinding.FragmentInisBinding;

public class IniSFragment extends Fragment {

    private FragmentInisBinding binding;

    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        IniSViewModel IniSViewModel =
                new ViewModelProvider(this).get(IniSViewModel.class);

        binding = FragmentInisBinding.inflate(inflater, container, false);
        View root = binding.getRoot();

        final TextView textView = binding.textIniS;
        IniSViewModel.getText().observe(getViewLifecycleOwner(), textView::setText);
        return root;
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }
}
