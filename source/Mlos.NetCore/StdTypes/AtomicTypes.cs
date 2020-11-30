// -----------------------------------------------------------------------
// <copyright file="AtomicTypes.cs" company="Microsoft Corporation">
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License. See LICENSE in the project root
// for license information.
// </copyright>
// -----------------------------------------------------------------------

using System;
using System.Diagnostics.CodeAnalysis;
using System.Runtime.CompilerServices;
using System.Threading;

using Mlos.Core;
using Mlos.Core.Collections;

using MlosStdTypes = global::Mlos.SettingsSystem.StdTypes;

namespace Proxy.Mlos.SettingsSystem.StdTypes
{
    /// <summary>
    /// Codegen proxy for std::atomic_bool.
    /// </summary>
    public struct AtomicBool : ICodegenProxy<MlosStdTypes.AtomicBool, AtomicBool>, IEquatable<AtomicBool>, IEquatable<MlosStdTypes.AtomicBool>
    {
        /// <summary>
        /// Operator ==.
        /// </summary>
        /// <param name="left"></param>
        /// <param name="right"></param>
        /// <returns></returns>
        public static bool operator ==(AtomicBool left, AtomicBool right) => left.Equals(right);

        /// <summary>
        /// Operator !=.
        /// </summary>
        /// <param name="left"></param>
        /// <param name="right"></param>
        /// <returns></returns>
        public static bool operator !=(AtomicBool left, AtomicBool right) => !(left == right);

        /// <summary>
        /// Operator ==.
        /// </summary>
        /// <param name="left"></param>
        /// <param name="right"></param>
        /// <returns></returns>
        public static bool operator ==(AtomicBool left, MlosStdTypes.AtomicBool right) => left.Equals(right);

        /// <summary>
        /// Operator !=.
        /// </summary>
        /// <param name="left"></param>
        /// <param name="right"></param>
        /// <returns></returns>
        public static bool operator !=(AtomicBool left, MlosStdTypes.AtomicBool right) => !(left == right);

        /// <inheritdoc />
        public override bool Equals(object obj)
        {
            if (obj is AtomicBool)
            {
                return Equals((AtomicBool)obj);
            }
            else if (obj is MlosStdTypes.AtomicBool)
            {
                return Equals((MlosStdTypes.AtomicBool)obj);
            }

            return false;
        }

        /// <inheritdoc />
        public bool Equals(AtomicBool other)
        {
            unsafe
            {
                return ptr == other.ptr;
            }
        }

        /// <inheritdoc />
        public bool Equals(MlosStdTypes.AtomicBool other)
        {
            return Load() == other.Value;
        }

        /// <inheritdoc />
        public override int GetHashCode()
        {
            unsafe
            {
                return (int)ptr;
            }
        }

        /// <summary>
        /// Returns a bool value, loaded as an atomic operation.
        /// </summary>
        /// <returns></returns>
        [MethodImpl(MethodImplOptions.AggressiveInlining)]
        public bool Load()
        {
            unsafe
            {
                return Volatile.Read(ref *ptr);
            }
        }

        /// <summary>
        /// Returns a bool value.
        /// </summary>
        /// <returns></returns>
        [MethodImpl(MethodImplOptions.AggressiveInlining)]
        public bool LoadRelaxed()
        {
            unsafe
            {
                return *ptr;
            }
        }

        /// <summary>
        /// Stores a bool value.
        /// </summary>
        /// <param name="value"></param>
        [MethodImpl(MethodImplOptions.AggressiveInlining)]
        public void Store(bool value)
        {
            unsafe
            {
                Volatile.Write(ref *ptr, value);
            }
        }

        /// <inheritdoc/>
        uint ICodegenKey.CodegenTypeIndex() => throw new NotImplementedException();

        /// <inheritdoc/>
        ulong ICodegenKey.CodegenTypeHash() => throw new NotImplementedException();

        /// <inheritdoc/>
        public ulong CodegenTypeSize() => sizeof(bool);

        /// <inheritdoc/>
        public uint GetKeyHashValue<THash>()
            where THash : IHash<uint> => throw new NotImplementedException();

        /// <inheritdoc/>
        public bool CompareKey(ICodegenProxy proxy) => throw new NotImplementedException();

        /// <inheritdoc/>
        bool ICodegenProxy.VerifyVariableData(ulong objectOffset, ulong totalDataSize, ref ulong expectedDataOffset) => true;

        /// <inheritdoc/>
        public IntPtr Buffer
        {
            get
            {
                unsafe
                {
                    return new IntPtr(ptr);
                }
            }

            set
            {
                unsafe
                {
                    ptr = (bool*)value.ToPointer();
                }
            }
        }

        private unsafe bool* ptr;
    }

    /// <summary>
    /// Codegen proxy for std::atomic_int32_t.
    /// </summary>
    public struct AtomicInt32 : ICodegenProxy<MlosStdTypes.AtomicInt32, AtomicInt32>, IEquatable<AtomicInt32>, IEquatable<MlosStdTypes.AtomicInt32>
    {
        /// <summary>
        /// Operator ==.
        /// </summary>
        /// <param name="left"></param>
        /// <param name="right"></param>
        /// <returns></returns>
        public static bool operator ==(AtomicInt32 left, AtomicInt32 right) => left.Equals(right);

        /// <summary>
        /// Operator ==.
        /// </summary>
        /// <param name="left"></param>
        /// <param name="right"></param>
        /// <returns></returns>
        public static bool operator ==(AtomicInt32 left, MlosStdTypes.AtomicInt32 right) => left.Equals(right);

        /// <summary>
        /// Operator !=.
        /// </summary>
        /// <param name="left"></param>
        /// <param name="right"></param>
        /// <returns></returns>
        public static bool operator !=(AtomicInt32 left, AtomicInt32 right) => !(left == right);

        /// <summary>
        /// Operator !=.
        /// </summary>
        /// <param name="left"></param>
        /// <param name="right"></param>
        /// <returns></returns>
        public static bool operator !=(AtomicInt32 left, MlosStdTypes.AtomicInt32 right) => !(left == right);

        /// <inheritdoc />
        public override bool Equals(object obj)
        {
            if (obj is AtomicInt32)
            {
                return Equals((AtomicInt32)obj);
            }
            else if (obj is MlosStdTypes.AtomicInt32)
            {
                return Equals((MlosStdTypes.AtomicInt32)obj);
            }

            return false;
        }

        /// <inheritdoc />
        public bool Equals(AtomicInt32 other)
        {
            unsafe
            {
                return ptr == other.ptr;
            }
        }

        /// <inheritdoc />
        public bool Equals(MlosStdTypes.AtomicInt32 other)
        {
            return Load() == other.Value;
        }

        /// <inheritdoc />
        public override int GetHashCode()
        {
            unsafe
            {
                return (int)ptr;
            }
        }

        /// <summary>
        /// Returns a 32-bit value, loaded as an atomic operation.
        /// </summary>
        /// <returns></returns>
        [MethodImpl(MethodImplOptions.AggressiveInlining)]
        public int Load()
        {
            unsafe
            {
                return Volatile.Read(ref *ptr);
            }
        }

        /// <summary>
        /// Returns a 32-bit value, loaded as an atomic operation.
        /// </summary>
        /// <returns></returns>
        [MethodImpl(MethodImplOptions.AggressiveInlining)]
        public int LoadRelaxed()
        {
            unsafe
            {
                return *ptr;
            }
        }

        /// <summary>
        /// Stores 32-bit value.
        /// </summary>
        /// <param name="value"></param>
        [MethodImpl(MethodImplOptions.AggressiveInlining)]
        internal void Store(int value)
        {
            unsafe
            {
                Volatile.Write(ref *ptr, value);
            }
        }

        /// <summary>
        /// Atomically compares two 32-bit signed integers for equality and, if they are equal, replaces the first value.
        /// </summary>
        /// <param name="value"></param>
        /// <param name="comparand"></param>
        /// <returns></returns>
        [MethodImpl(MethodImplOptions.AggressiveInlining)]
        public int CompareExchange(int value, int comparand)
        {
            unsafe
            {
                return Interlocked.CompareExchange(ref *ptr, value, comparand);
            }
        }

        /// <inheritdoc/>
        uint ICodegenKey.CodegenTypeIndex() => throw new NotImplementedException();

        /// <inheritdoc/>
        ulong ICodegenKey.CodegenTypeHash() => throw new NotImplementedException();

        /// <inheritdoc/>
        public ulong CodegenTypeSize() => sizeof(int);

        /// <inheritdoc/>
        public uint GetKeyHashValue<THash>()
            where THash : IHash<uint> => throw new NotImplementedException();

        /// <inheritdoc/>
        public bool CompareKey(ICodegenProxy proxy) => throw new NotImplementedException();

        /// <inheritdoc/>
        bool ICodegenProxy.VerifyVariableData(ulong objectOffset, ulong totalDataSize, ref ulong expectedDataOffset) => true;

        /// <inheritdoc/>
        public IntPtr Buffer
        {
            get
            {
                unsafe
                {
                    return new IntPtr(ptr);
                }
            }

            set
            {
                unsafe
                {
                    ptr = (int*)value.ToPointer();
                }
            }
        }

        private unsafe int* ptr;
    }

    /// <summary>
    /// Codegen proxy for std::atomic_uint32_t.
    /// </summary>
    public struct AtomicUInt32 : ICodegenProxy<MlosStdTypes.AtomicUInt32, AtomicUInt32>, IEquatable<AtomicUInt32>, IEquatable<MlosStdTypes.AtomicUInt32>
    {
        /// <summary>
        /// Operator ==.
        /// </summary>
        /// <param name="left"></param>
        /// <param name="right"></param>
        /// <returns></returns>
        public static bool operator ==(AtomicUInt32 left, AtomicUInt32 right) => left.Equals(right);

        /// <summary>
        /// Operator ==.
        /// </summary>
        /// <param name="left"></param>
        /// <param name="right"></param>
        /// <returns></returns>
        public static bool operator ==(AtomicUInt32 left, MlosStdTypes.AtomicUInt32 right) => left.Equals(right);

        /// <summary>
        /// Operator !=.
        /// </summary>
        /// <param name="left"></param>
        /// <param name="right"></param>
        /// <returns></returns>
        public static bool operator !=(AtomicUInt32 left, AtomicUInt32 right) => !(left == right);

        /// <summary>
        /// Operator !=.
        /// </summary>
        /// <param name="left"></param>
        /// <param name="right"></param>
        /// <returns></returns>
        public static bool operator !=(AtomicUInt32 left, MlosStdTypes.AtomicUInt32 right) => !(left == right);

        /// <inheritdoc />
        public override bool Equals(object obj)
        {
            if (obj is AtomicUInt32)
            {
                return Equals((AtomicUInt32)obj);
            }
            else if (obj is MlosStdTypes.AtomicUInt32)
            {
                return Equals((MlosStdTypes.AtomicUInt32)obj);
            }

            return false;
        }

        /// <inheritdoc />
        public bool Equals(AtomicUInt32 other)
        {
            unsafe
            {
                return ptr == other.ptr;
            }
        }

        /// <inheritdoc />
        public bool Equals(MlosStdTypes.AtomicUInt32 other)
        {
            return Load() == other.Value;
        }

        /// <inheritdoc />
        public override int GetHashCode()
        {
            unsafe
            {
                return (int)ptr;
            }
        }

        /// <summary>
        /// Returns a 32-bit value, loaded as an atomic operation.
        /// </summary>
        /// <returns></returns>
        [MethodImpl(MethodImplOptions.AggressiveInlining)]
        public uint Load()
        {
            unsafe
            {
                return Volatile.Read(ref *ptr);
            }
        }

        /// <summary>
        /// Returns a 32-bit value.
        /// </summary>
        /// <returns></returns>
        [MethodImpl(MethodImplOptions.AggressiveInlining)]
        public uint LoadRelaxed()
        {
            unsafe
            {
                return *ptr;
            }
        }

        /// <summary>
        /// Stores 32-bit value.
        /// </summary>
        /// <param name="value"></param>
        [MethodImpl(MethodImplOptions.AggressiveInlining)]
        internal void Store(uint value)
        {
            unsafe
            {
                Volatile.Write(ref *ptr, value);
            }
        }

        /// <summary>
        /// Increments a specified variable and stores the result, as an atomic operation.
        /// </summary>
        /// <returns></returns>
        [MethodImpl(MethodImplOptions.AggressiveInlining)]
        public AtomicUInt32 Increment()
        {
            unsafe
            {
                Interlocked.Increment(ref *(int*)ptr);
                return this;
            }
        }

        /// <summary>
        /// Atomically compares two 32-bit unsigned integers for equality and, if they are equal, replaces the first value.
        /// </summary>
        /// <param name="value"></param>
        /// <param name="comparand"></param>
        /// <returns></returns>
        [MethodImpl(MethodImplOptions.AggressiveInlining)]
        public uint CompareExchange(uint value, uint comparand)
        {
            unsafe
            {
                return (uint)Interlocked.CompareExchange(ref *(int*)ptr, (int)value, (int)comparand);
            }
        }

        [MethodImpl(MethodImplOptions.AggressiveInlining)]
        internal uint FetchAdd(uint value)
        {
            unsafe
            {
                return (uint)Interlocked.Add(ref *(int*)ptr, (int)value);
            }
        }

        [MethodImpl(MethodImplOptions.AggressiveInlining)]
        internal uint FetchSub(uint value)
        {
            unsafe
            {
                return (uint)Interlocked.Add(ref *(int*)ptr, -(int)value);
            }
        }

        /// <inheritdoc/>
        uint ICodegenKey.CodegenTypeIndex() => throw new NotImplementedException();

        /// <inheritdoc/>
        ulong ICodegenKey.CodegenTypeHash() => throw new NotImplementedException();

        /// <inheritdoc/>
        public ulong CodegenTypeSize() => sizeof(uint);

        /// <inheritdoc/>
        public uint GetKeyHashValue<THash>()
            where THash : IHash<uint> => throw new NotImplementedException();

        /// <inheritdoc/>
        public bool CompareKey(ICodegenProxy proxy) => throw new NotImplementedException();

        /// <inheritdoc/>
        bool ICodegenProxy.VerifyVariableData(ulong objectOffset, ulong totalDataSize, ref ulong expectedDataOffset) => true;

        /// <inheritdoc/>
        public IntPtr Buffer
        {
            get
            {
                unsafe
                {
                    return new IntPtr(ptr);
                }
            }

            set
            {
                unsafe
                {
                    ptr = (uint*)value.ToPointer();
                }
            }
        }

        private unsafe uint* ptr;
    }

    /// <summary>
    /// Codegen proxy for std::atomic_int64_t.
    /// </summary>
    public struct AtomicUInt64 : ICodegenProxy<MlosStdTypes.AtomicUInt64, AtomicUInt64>, IEquatable<AtomicUInt64>, IEquatable<MlosStdTypes.AtomicUInt64>
    {
        /// <summary>
        /// Operator ==.
        /// </summary>
        /// <param name="left"></param>
        /// <param name="right"></param>
        /// <returns></returns>
        public static bool operator ==(AtomicUInt64 left, AtomicUInt64 right) => left.Equals(right);

        /// <summary>
        /// Operator !=.
        /// </summary>
        /// <param name="left"></param>
        /// <param name="right"></param>
        /// <returns></returns>
        public static bool operator !=(AtomicUInt64 left, AtomicUInt64 right) => !(left == right);

        /// <summary>
        /// Operator ==.
        /// </summary>
        /// <param name="left"></param>
        /// <param name="right"></param>
        /// <returns></returns>
        public static bool operator ==(AtomicUInt64 left, MlosStdTypes.AtomicUInt64 right) => left.Equals(right);

        /// <summary>
        /// Operator !=.
        /// </summary>
        /// <param name="left"></param>
        /// <param name="right"></param>
        /// <returns></returns>
        public static bool operator !=(AtomicUInt64 left, MlosStdTypes.AtomicUInt64 right) => !(left == right);

        /// <inheritdoc />
        public override bool Equals(object obj)
        {
            if (obj is AtomicUInt64)
            {
                return Equals((AtomicUInt64)obj);
            }
            else if (obj is MlosStdTypes.AtomicUInt64)
            {
                return Equals((MlosStdTypes.AtomicUInt64)obj);
            }

            return false;
        }

        /// <inheritdoc />
        public bool Equals(AtomicUInt64 other)
        {
            unsafe
            {
                return ptr == other.ptr;
            }
        }

        /// <inheritdoc />
        public bool Equals(MlosStdTypes.AtomicUInt64 other)
        {
            unsafe
            {
                return Load() == other.Value;
            }
        }

        /// <inheritdoc />
        public override int GetHashCode()
        {
            unsafe
            {
                return (int)ptr;
            }
        }

        /// <summary>
        /// Returns a 64-bit value, loaded as an atomic operation.
        /// </summary>
        /// <returns></returns>
        [MethodImpl(MethodImplOptions.AggressiveInlining)]
        public ulong Load()
        {
            unsafe
            {
                return Volatile.Read(ref *ptr);
            }
        }

        /// <summary>
        /// Returns a 64-bit value.
        /// </summary>
        /// <returns></returns>
        [MethodImpl(MethodImplOptions.AggressiveInlining)]
        public ulong LoadRelaxed()
        {
            unsafe
            {
                return *ptr;
            }
        }

        /// <summary>
        /// Stores 64-bit value.
        /// </summary>
        /// <param name="value"></param>
        [MethodImpl(MethodImplOptions.AggressiveInlining)]
        internal void Store(ulong value)
        {
            unsafe
            {
                Volatile.Write(ref *ptr, value);
            }
        }

        /// <summary>
        /// Atomically compares two 64-bit unsigned integers for equality and, if they are equal, replaces the first value.
        /// </summary>
        /// <param name="value"></param>
        /// <param name="comparand"></param>
        /// <returns></returns>
        [MethodImpl(MethodImplOptions.AggressiveInlining)]
        public ulong CompareExchange(ulong value, ulong comparand)
        {
            unsafe
            {
                return (ulong)Interlocked.CompareExchange(ref *(long*)ptr, (long)value, (long)comparand);
            }
        }

        /// <inheritdoc/>
        uint ICodegenKey.CodegenTypeIndex() => throw new NotImplementedException();

        /// <inheritdoc/>
        ulong ICodegenKey.CodegenTypeHash() => throw new NotImplementedException();

        /// <inheritdoc/>
        public ulong CodegenTypeSize() => sizeof(ulong);

        /// <inheritdoc/>
        public uint GetKeyHashValue<THash>()
            where THash : IHash<uint> => throw new NotImplementedException();

        /// <inheritdoc/>
        public bool CompareKey(ICodegenProxy proxy) => throw new NotImplementedException();

        /// <inheritdoc/>
        bool ICodegenProxy.VerifyVariableData(ulong objectOffset, ulong totalDataSize, ref ulong expectedDataOffset) => true;

        /// <inheritdoc/>
        public IntPtr Buffer
        {
            get
            {
                unsafe
                {
                    return new IntPtr(ptr);
                }
            }

            set
            {
                unsafe
                {
                    ptr = (ulong*)value.ToPointer();
                }
            }
        }

        private unsafe ulong* ptr;
    }
}
